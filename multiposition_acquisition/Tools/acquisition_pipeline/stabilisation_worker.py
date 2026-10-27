import numpy as np
import os
from skimage.registration import phase_cross_correlation as pcc
import time

from PySide6.QtCore import QObject, Signal, Slot

from image_analysis.Deskew_Numpy import deskew_numpy, compute_px_shift

class Stabilisation_Worker(QObject):
    
    def __init__(self, worker, positions, channel, aspect_ratio, angle, binning, px_size, save_dir):
        """
        Initialize the stabilization worker and connect it to the acquisition pipeline.
        
        Parameters
        ----------
        worker : AcquisitionWorker
            Worker providing acquired 3D volumes.
        positions : Positions
            Shared acquisition positions, in millimeters.
        channel : str
            Channel used for stabilization.
        aspect_ratio : float
            Axial-to-lateral pixel size ratio.
        angle : float
            Oblique plane angle, in degrees.
        binning : int
            Camera binning factor.
        px_size : float
            Pixel size in sample space, in micrometers.
        save_dir : str
            Directory used to save correction logs.
        """
        super().__init__()
        self.positions = positions
        self.channel = channel
        self.aspect_ratio = aspect_ratio
        self.angle = angle
        self.binning = binning
        self.px_size = px_size
        self.save_dir = save_dir
        
        self.px_shift = compute_px_shift(aspect_ratio, angle, binning, unit="deg")
        self.on_init()
                
        # Create porjection images datas
        self.projections = [
            {"first_max_front" : None,
             "new_max_front" : None,
             "first_max_side"  : None,
             "new_max_side"  : None}
            for _ in range(self.positions.get_active_positions())]
        
        self.total_displacement = [
            {"x" : 0,
             "y" : 0,
             "z" : 0}
            for _ in range(self.positions.get_active_positions())            ]
        
        worker.new_volume_ready.connect(self.volume_recieved)
        worker.set_preview_callback()
        
    def on_init(self):
        pass
    
    @Slot(np.ndarray, dict)
    def volume_recieved(self, volume, metadata):
        """
        Process an acquired volume and estimate sample drift.
        
        Parameters
        ----------
        volume : np.ndarray
            Acquired 3D image (Z, Y, X).
        metadata : dict
            Acquisition metadata containing position and channel information.
        
        Notes
        -----
        
        This method is connected to the new_volume_ready Qt signal.
        """
        
        position, channel = metadata["channel"].split("_") #metadata.channel is composed of position_channel
        position = int(position)
        
        if channel != self.channel :
            return
        
        deskewed_volume = deskew_numpy(volume, px_shift_y=self.px_shift)
        
        max_front = np.max(deskewed_volume, axis = 0)
        max_side = np.max(deskewed_volume, axis = 2)
        
        del volume
        
        self._add_projection(position, max_front, max_side)
        
        self._compute_displacement(position)
            
    
    # TODO inutile, a supprimer
    def get_positions(self):
        return self.positions
    
    def _add_projection(self, position, max_front, max_side):
        """
        Store the maximum intensity projections for an acquisition position.
        
        The first pair of projections received for a position is stored
        as the reference. Subsequent projections replace the previous
        measurement while preserving the original reference.
        
        Parameters
        ----------
        position : int
            Zero-based index of the acquisition position.
        max_front : numpy.ndarray
            2D maximum intensity projection along axis 0 of the
            deskewed volume, corresponding to the front view.
        max_side : numpy.ndarray
            2D maximum intensity projection along axis 2 of the
            deskewed volume, corresponding to the side view.
        """
        if self.projections[position]["first_max_front"] is None and self.projections[position]["first_max_side"] is None :
            self.projections[position]["first_max_front"] = max_front
            self.projections[position]["first_max_side"] = max_side
            
        else :
            self.projections[position]["new_max_front"] = max_front
            self.projections[position]["new_max_side"] = max_side 
        
    
    def _compute_displacement(self, position):
        """
        Calculate sample drift relative to the first volume and update stage positions.
        
        The resulting displacements are transformed into the stage
        coordinate system and converted from micrometers to millimeters.

        Parameters
        ----------
        position : int
            Acquisition position index.
        
        Notes
        -----
        Displacements are estimated by phase cross-correlation and
        converted into stage coordinates in millimeters.
        
        The calculation is skipped if any required reference or current
        projection is missing.
        
        The reference projections remain unchanged throughout acquisition,
        so the estimated displacement is relative to the first volume
        acquired at the corresponding position.
        
        Only the X displacement from the front projection is used.
        The side projection provides the components used to calculate
        the Y and Z stage displacements.
        """
        if self.projections[position]["first_max_front"] is None :
            return
        if self.projections[position]["new_max_front"] is None :
            return
        if self.projections[position]["first_max_side"] is None:
            return
        if self.projections[position]["new_max_side"] is None :
            return
        
        shift_front, _, _ = pcc(
            self.projections[position]["first_max_front"],
            self.projections[position]["new_max_front"],
            upsample_factor = 1 )
        
        dy_front, dx_front = shift_front
        dy_front = dy_front * self.px_size * self.binning
        dx_front = dx_front * self.px_size * self.binning
        
        shift_side, _, _ = pcc(
            self.projections[position]["first_max_side"],
            self.projections[position]["new_max_side"],
            upsample_factor = 1 )
        
        dy_side, dx_side = shift_side
        dy_side = dy_side * self.aspect_ratio * self.px_size * self.binning
        dx_side = dx_side * self.px_size * self.binning
        
        # print(f"Position :{position}\n -dy front : {dy_front}\n -dx front : {dx_front}\n -dy side : {dy_side}\n -dx side : {dx_side}")
        
        # theta = np.deg2rad(270-self.angle)
        theta = np.deg2rad(90+self.angle)
        cos, sin = np.cos(theta), np.sin(theta)
        dx_mean = (dx_side + dy_front) / 2 # Use o
        
        dx_stage = - dx_front / 1000
        # dy_stage = (- dx_side * sin + dy_side * cos) / 1000
        # dz_stage = (dx_side * cos + dy_side * sin) / 1000
        dy_stage = (- dx_mean * sin + dy_side * cos) / 1000
        dz_stage = (dx_mean * cos + dy_side * sin) / 1000
        
        # print(f"Position : {position}\n -dx stage : {dx_stage}\n -dy stage : {dy_stage}\n -dz stage = {dz_stage}")
        
        dx_stage, dy_stage, dz_stage  = self._test_displacement(position, dx_stage, dy_stage, dz_stage)
        
        self.save_correction(position, dx_stage, dy_stage, dz_stage)
        
        self.positions[position].x += - dx_stage
        self.positions[position].y += - dy_stage
        self.positions[position].z += - dz_stage
        
        self.total_displacement[position]["x"] += dx_stage
        self.total_displacement[position]["y"] += dy_stage
        self.total_displacement[position]["z"] += dz_stage
        
    def _test_displacement(self, position, dx, dy, dz,
                           max_dx = 0.050, max_dy = 0.050, max_dz = 0.050,
                           max_total_dx = 1.0, max_total_dy = 1.0, max_total_dz = 1.0) :
        """
        Limit individual corrections and reject excessive cumulative drift.
        
        Parameters
        ----------
        position : int
            Acquisition position index.
        dx, dy, dz : float
            Measured displacements in millimeters.
        max_dx, max_dy, max_dz : float, optional
            Maximum correction per measurement. Default is 0.050 mm.
        max_total_dx, max_total_dy, max_total_dz : float, optional
            Maximum cumulative correction. Default is 1.0 mm.
        
        Returns
        -------
        dx, dy, dz : float
            Validated displacements in millimeters.
        """
        dx = max(min(dx,max_dx),-max_dx)
        dy = max(min(dy,max_dy),-max_dy)
        dz = max(min(dz,max_dz),-max_dz)
        
        if not - max_total_dx < self.total_displacement[position]["x"] + dx < max_total_dx :
            dx = 0
        
        if not - max_total_dy < self.total_displacement[position]["y"] + dy < max_total_dy :
            dy = 0
            
        if not - max_total_dz < self.total_displacement[position]["z"] + dz < max_total_dz :
            dz = 0
            
        return dx, dy, dz
    
    def save_correction(self, position, dx, dy, dz):
        """
        Append the stabilization correction to Position_corrections.txt.
        
        Parameters
        ----------
        position : int
            Acquisition position index.
        dx, dy, dz : float
            Measured displacements in millimeters.
        """
        
        file_path = os.path.join(self.save_dir, "Position_corrections.txt")
        
        current_time = time.strftime("%H:%M:%S")
        
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f'{current_time},Position {position},{dx:.6f},{dy:.6f},{dz:.6f}\n')
            file.flush()
