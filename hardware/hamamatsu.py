#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A ctypes based interface to Hamamatsu cameras.
(tested on a sCMOS Flash 4.0).

The documentation is a little confusing to me on this subject..
I used c_int32 when this is explicitly specified, otherwise I use c_int.

Hazen 10/13

George 11/17 - Updated for SDK4 and to allow fixed length acquisition
"""

import ctypes
import ctypes.util
import numpy
import time
import warnings

# from progressbar import printProgressBar

# Hamamatsu constants.

# DCAM4 API.
DCAMERR_ERROR = 0
DCAMERR_NOERROR = 1

DCAMPROP_ATTR_HASVALUETEXT = int("0x10000000", 0)
DCAMPROP_ATTR_READABLE = int("0x00010000", 0)
DCAMPROP_ATTR_WRITABLE = int("0x00020000", 0)

DCAMPROP_OPTION_NEAREST = int("0x80000000", 0)
DCAMPROP_OPTION_NEXT = int("0x01000000", 0)
DCAMPROP_OPTION_SUPPORT = int("0x00000000", 0)

DCAMPROP_TYPE_MODE = int("0x00000001", 0)
DCAMPROP_TYPE_LONG = int("0x00000002", 0)
DCAMPROP_TYPE_REAL = int("0x00000003", 0)
DCAMPROP_TYPE_MASK = int("0x0000000F", 0)

DCAMCAP_STATUS_ERROR = int("0x00000000", 0)
DCAMCAP_STATUS_BUSY = int("0x00000001", 0)
DCAMCAP_STATUS_READY = int("0x00000002", 0)
DCAMCAP_STATUS_STABLE = int("0x00000003", 0)
DCAMCAP_STATUS_UNSTABLE = int("0x00000004", 0)

DCAMWAIT_CAPEVENT_FRAMEREADY = int("0x0002", 0)
DCAMWAIT_CAPEVENT_STOPPED = int("0x0010", 0)

DCAMWAIT_RECEVENT_MISSED = int("0x00000200", 0)
DCAMWAIT_RECEVENT_STOPPED = int("0x00000400", 0)
DCAMWAIT_TIMEOUT_INFINITE = int("0x80000000", 0)

DCAM_DEFAULT_ARG = 0

# DCAM_IDSTR
DCAM_IDSTR_CAMERAID = int("0x04000102", 0)
DCAM_IDSTR_VENDOR = int("0x04000103", 0)
DCAM_IDSTR_MODEL = int("0x04000104", 0)
DCAM_IDSTR_CAMERAVERSION = int("0x04000105", 0)
DCAM_IDSTR_DRIVERVERSION = int("0x04000106", 0)
DCAM_IDSTR_MODULEVERSION = int("0x04000107", 0)
DCAM_IDSTR_DCAMAPIVERSION = int("0x04000108", 0)

DCAMCAP_TRANSFERKIND_FRAME = 0

DCAMCAP_START_SEQUENCE = -1
DCAMCAP_START_SNAP = 0

DCAMBUF_ATTACHKIND_FRAME = 0


# Hamamatsu structures.

# # DCAMAPI_INIT
#
# The dcam initialization structure
#
class DCAMAPI_INIT(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int32),
                ("iDeviceCount", ctypes.c_int32),
                ("reserved", ctypes.c_int32),
                ("initoptionbytes", ctypes.c_int32),
                ("initoption", ctypes.POINTER(ctypes.c_int32)),
                ("guid", ctypes.POINTER(ctypes.c_int32))]


# # DCAMDEV_OPEN
#
# The dcam open structure
#
class DCAMDEV_OPEN(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int32),
                ("index", ctypes.c_int32),
                ("hdcam", ctypes.c_void_p)]


# # DCAMWAIT_OPEN
#
# The dcam wait open structure
#
class DCAMWAIT_OPEN(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int32),
                ("supportevent", ctypes.c_int32),
                ("hwait", ctypes.c_void_p),
                ("hdcam", ctypes.c_void_p)]


# # DCAMWAIT_START
#
# The dcam wait start structure
#
class DCAMWAIT_START(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int32),
                ("eventhappened", ctypes.c_int32),
                ("eventmask", ctypes.c_int32),
                ("timeout", ctypes.c_int32)]


# # DCAMCAP_TRANSFERINFO
#
# The dcam capture info structure
#
class DCAMCAP_TRANSFERINFO(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int32),
                ("iKind", ctypes.c_int32),
                ("nNewestFrameIndex", ctypes.c_int32),
                ("nFrameCount", ctypes.c_int32)]


# # DCAMBUF_ATTACH
#
# The dcam buffer attachment structure
#
class DCAMBUF_ATTACH(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int32),
                ("iKind", ctypes.c_int32),
                ("buffer", ctypes.POINTER(ctypes.c_void_p)),
                ("buffercount", ctypes.c_int32)]


# # DCAM_TIMESTAMP
#
# The dcam timestamp frame structure
#
class DCAM_TIMESTAMP(ctypes.Structure):
    _fields_ = [("sec", ctypes.c_int32),
                ("microsec", ctypes.c_int32)]


# # DCAMBUF_FRAME
#
# The dcam buffer frame structure
#
class DCAMBUF_FRAME(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int32),
                ("iKind", ctypes.c_int32),
                ("option", ctypes.c_int32),
                ("iFrame", ctypes.c_int32),
                ("buf", ctypes.c_void_p),
                ("rowbytes", ctypes.c_int32),
                ("type", ctypes.c_int32),
                ("width", ctypes.c_int32),
                ("height", ctypes.c_int32),
                ("left", ctypes.c_int32),
                ("top", ctypes.c_int32),
                ("timestamp", DCAM_TIMESTAMP),
                ("framestamp", ctypes.c_int32),
                ("camerastamp", ctypes.c_int32)]


# # DCAMDEV_STRING
#
# The dcam device string structure
#
class DCAMDEV_STRING(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int32),
                ("iString", ctypes.c_int32),
                ("text", ctypes.c_char_p),
                ("textbytes", ctypes.c_int32)]


# # DCAMPROP_ATTR
#
# The dcam property attribute structure.
#
class DCAMPROP_ATTR(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_int32),
                ("iProp", ctypes.c_int32),
                ("option", ctypes.c_int32),
                ("iReserved1", ctypes.c_int32),
                ("attribute", ctypes.c_int32),
                ("iGroup", ctypes.c_int32),
                ("iUnit", ctypes.c_int32),
                ("attribute2", ctypes.c_int32),
                ("valuemin", ctypes.c_double),
                ("valuemax", ctypes.c_double),
                ("valuestep", ctypes.c_double),
                ("valuedefault", ctypes.c_double),
                ("nMaxChannel", ctypes.c_int32),
                ("iReserved3", ctypes.c_int32),
                ("nMaxView", ctypes.c_int32),
                ("iProp_NumberOfElement", ctypes.c_int32),
                ("iProp_ArrayBase", ctypes.c_int32),
                ("iPropStep_Element", ctypes.c_int32)]


# # DCAMPROP_VALUETEXT
#
# The dcam text property structure.
#
class DCAMPROP_VALUETEXT(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_int32),
                ("iProp", ctypes.c_int32),
                ("value", ctypes.c_double),
                ("text", ctypes.c_char_p),
                ("textbytes", ctypes.c_int32)]


def convertPropertyName(p_name):
    """
    "Regularizes" a property name. We are using all lowercase names with
    the spaces replaced by underscores.
    """
    return p_name.lower().replace(" ", "_")


class DCAMException(Exception):
    pass


class HCamData(object):
    """
    Hamamatsu camera data object.

    Initially I tried to use create_string_buffer() to allocate storage for the
    data from the camera but this turned out to be too slow. The software
    kept falling behind the camera and create_string_buffer() seemed to be the
    bottleneck.

    Using numpy makes a lot more sense anyways..
    """

    def __init__(self, size=None, **kwds):
        """
        Create a data object of the appropriate size.
        """
        super().__init__(**kwds)
        self.np_array = numpy.ascontiguousarray(numpy.empty(int(size / 2), dtype=numpy.uint16))
        self.size = size

    def __getitem__(self, slice):
        return self.np_array[slice]

    def copyData(self, address):
        """
        Uses the C memmove function to copy data from an address in memory
        into memory allocated for the numpy array of this object.

        ctypes.memmove(dst, src, count) copies count bytes from src to dst.
        dst and src must be integers or ctypes instances that can be
        converted to pointers.
        """
        ctypes.memmove(self.np_array.ctypes.data, address, self.size)

    def getData(self):
        return self.np_array

    def getDataPtr(self):
        return self.np_array.ctypes.data


class HamamatsuCamera(object):
    """
    Basic camera interface class.

    This version uses the Hamamatsu library to allocate camera buffers.
    Storage for the data from the camera is allocated dynamically and
    copied out of the camera buffers.
    """

    def __init__(self, data_buffers=None, locks=None, **kwds):
        """
        Open the connection to the camera specified by camera_id.
        """
        super().__init__()

        #
        # Initialization of the API
        #
        self._dcam = ctypes.windll.dcamapi

        paraminit = DCAMAPI_INIT(0, 0, 0, 0, None, None)
        paraminit.size = ctypes.sizeof(paraminit)
        error_code = self._dcam.dcamapi_init(ctypes.byref(paraminit))
        if error_code != DCAMERR_NOERROR:
            raise DCAMException("DCAM initialization failed with error code " + str(error_code))

        self.n_cameras = paraminit.iDeviceCount
        self.camera_ids = list(range(self.n_cameras))
        self.encoding = 'utf-8'
        self.camera = [self.Camera(self, camera_id=i) for i in self.camera_ids]
        for camera_id in self.camera_ids:
            self.camera[camera_id].load_properties()
            self.camera[camera_id].load_camera_infos()
        self.data_buffers = data_buffers
        self.locks = locks

    class Camera(object):

        def __init__(self, hcam, camera_id=0):
            self.hcam = hcam  # handle for API
            self.camera_id = camera_id
            self.buffer_index = 0
            self.frame_bytes = 0
            self.frame_x = 0
            self.frame_y = 0
            self.last_frame_number = 0
            self.properties = None
            self.max_backlog = 0
            self.number_image_buffers = 0
            self.acquisition_mode = "run_till_abort"
            self.number_frames = 0
            self.ctrl_buff_index = -1
            self.ctrl_frame_number = -1

            # Open the camera.
            paramopen = DCAMDEV_OPEN(0, self.camera_id, None)
            paramopen.size = ctypes.sizeof(paramopen)
            self.hcam.checkStatus(self.hcam._dcam.dcamdev_open(ctypes.byref(paramopen)), "dcamdev_open", self.camera_id)
            self.handle = ctypes.c_void_p(paramopen.hdcam)

            # Set up wait handle
            paramwait = DCAMWAIT_OPEN(0, 0, None, self.handle)
            paramwait.size = ctypes.sizeof(paramwait)
            self.hcam.checkStatus(self.hcam._dcam.dcamwait_open(ctypes.byref(paramwait)), "dcamwait_open", self.camera_id)
            self.wait_handle = ctypes.c_void_p(paramwait.hwait)

            self.properties = {}

        def load_camera_infos(self):
            # Get camera info
            self.camera_manufacturer = self.hcam.getCameraManufacturer(self.camera_id)
            self.camera_model = self.hcam.getCameraModel(self.camera_id)
            self.camera_version = self.hcam.getCameraVersion(self.camera_id)
            self.camera_driver_version = self.hcam.getCameraDriverVersion(self.camera_id)
            self.camera_module_version = self.hcam.getCameraModuleVersion(self.camera_id)
            self.camera_api_version = self.hcam.getCameraAPIVersion(self.camera_id)

        def load_properties(self):
            # Get camera properties.
            self.properties = self.hcam.getCameraProperties(self.camera_id)
            self.hcam.addMissingProperties(self.properties)

            # Get camera max width, height.
            self.max_width = self.hcam.getPropertyValue("image_width", self.camera_id)[0]
            self.max_height = self.hcam.getPropertyValue("image_height", self.camera_id)[0]

        def set_properties(self, props):
            for key, value in zip(props.keys(), props.values()):
                self.hcam.setPropertyValue(self.handle, key, value, self.properties)

    def getProperties(self, camera_id):
        """
        Return the list of camera properties. This is the one to call if you
        want to know the camera properties.
        """
        return self.camera[camera_id].properties

    def getPropertyAttribute(self, property_name, camera_id):
        """
        Return the attribute structure of a particular property.
        """
        handle = self.camera[camera_id].handle
        properties = self.camera[camera_id].properties

        p_attr = DCAMPROP_ATTR()
        p_attr.cbSize = ctypes.sizeof(p_attr)
        p_attr.iProp = properties[property_name]
        ret = self.checkStatus(self._dcam.dcamprop_getattr(handle, ctypes.byref(p_attr)),
                               "dcamprop_getattr", camera_id)
        if (ret == 0):
            print("property", property_name, "is not supported")
            return False
        else:
            return p_attr

    def getPropertyRange(self, property_name, camera_id):
        """
        Return the range for an attribute.
        """
        prop_attr = self.getPropertyAttribute(property_name, camera_id)
        temp = prop_attr.attribute & DCAMPROP_TYPE_MASK
        if (temp == DCAMPROP_TYPE_REAL):
            return [float(prop_attr.valuemin), float(prop_attr.valuemax)]
        else:
            return [int(prop_attr.valuemin), int(prop_attr.valuemax)]

    def getPropertyRW(self, property_name, camera_id):
        """
        Return if a property is readable / writeable.
        """
        prop_attr = self.getPropertyAttribute(property_name, camera_id)
        rw = (prop_attr.is_readable(), prop_attr.is_writable())

        return rw

    def getPropertyDefaultValue(self, property_name, camera_id):
        """
        Return the default value of a RW property
        """
        properties = self.camera[camera_id].properties

        # Check if the property exists.
        if not (property_name in properties):
            print(" unknown property name:", property_name)
            return False

        # Get the property attributes.
        prop_attr = self.getPropertyAttribute(property_name, camera_id)
        if prop_attr.attribute & DCAMPROP_ATTR_WRITABLE:
            default_value = prop_attr.valuedefault
        else:
            raise TypeError('The attribute {} is not writeable'.format(property_name))

        return default_value

    def getAttributeType(self, property_name, camera_id):
        """
        Return the default value of a RW property
        """
        properties = self.camera[camera_id].properties
        # Check if the property exists.
        if not (property_name in properties):
            print(" unknown property name:", property_name)
            return False

        # Get the property attributes.
        prop_attr = self.getPropertyAttribute(property_name, camera_id)

        # get attribute type.
        temp = prop_attr.attribute & DCAMPROP_TYPE_MASK
        if (temp == DCAMPROP_TYPE_MODE):
            prop_type = "MODE"
        elif (temp == DCAMPROP_TYPE_LONG):
            prop_type = "LONG"
        elif (temp == DCAMPROP_TYPE_REAL):
            prop_type = "REAL"
        else:
            prop_type = "NONE"

        return prop_type

    def isPropertyWritable(self, property_name, camera_id):
        """
        Return True if the property is writable, return False otherwise
        """

        prop_attr = self.getPropertyAttribute(property_name, camera_id)
        is_writable = False

        # Check if the property is writable.
        if (prop_attr.attribute & DCAMPROP_ATTR_WRITABLE):
            is_writable = True

        return is_writable

    def getPropertyText(self, property_name,camera_id):
        """
        #Return the text options of a property (if any).
        """
        handle = self.camera[camera_id].handle
        properties = self.camera[camera_id].properties

        prop_attr = self.getPropertyAttribute(property_name, camera_id)
        if not (prop_attr.attribute & DCAMPROP_ATTR_HASVALUETEXT):
            return {}
        else:
            # Create property text structure.
            prop_id = properties[property_name]
            v = ctypes.c_double(prop_attr.valuemin)

            prop_text = DCAMPROP_VALUETEXT()
            c_buf_len = 64
            c_buf = ctypes.create_string_buffer(c_buf_len)
            # prop_text.text = ctypes.c_char_p(ctypes.addressof(c_buf))
            prop_text.cbSize = ctypes.c_int32(ctypes.sizeof(prop_text))
            prop_text.iProp = ctypes.c_int32(prop_id)
            prop_text.value = v
            prop_text.text = ctypes.addressof(c_buf)
            prop_text.textbytes = c_buf_len

            # Collect text options.
            done = False
            text_options = {}
            while not done:
                # Get text of current value.
                self.checkStatus(self._dcam.dcamprop_getvaluetext(handle, ctypes.byref(prop_text)),
                                 "dcamprop_getvaluetext", camera_id)
                text_options[prop_text.text.decode(self.encoding)] = int(v.value)

                # Get next value.
                ret = self._dcam.dcamprop_queryvalue(handle,
                                                     ctypes.c_int32(prop_id),
                                                     ctypes.byref(v),
                                                     ctypes.c_int32(DCAMPROP_OPTION_NEXT))
                prop_text.value = v

                if (ret != 1):
                    done = True

            return text_options

    def getPropertyValue(self, property_name, camera_id):
        """
        Return the current setting of a particular property.
        """
        handle = self.camera[camera_id].handle
        properties = self.camera[camera_id].properties

        # Check if the property exists.
        if not (property_name in properties):
            print(" unknown property name:", property_name)
            return False
        prop_id = properties[property_name]

        # Get the property attributes.
        prop_attr = self.getPropertyAttribute(property_name, camera_id)

        # Get the property value.
        c_value = ctypes.c_double(0)
        self.checkStatus(self._dcam.dcamprop_getvalue(handle,
                                                      ctypes.c_int32(prop_id),
                                                      ctypes.byref(c_value)),
                         "dcamprop_getvalue", camera_id)

        # Convert type based on attribute type.
        temp = prop_attr.attribute & DCAMPROP_TYPE_MASK
        if (temp == DCAMPROP_TYPE_MODE):
            prop_type = "MODE"
            prop_value = int(c_value.value)
        elif (temp == DCAMPROP_TYPE_LONG):
            prop_type = "LONG"
            prop_value = int(c_value.value)
        elif (temp == DCAMPROP_TYPE_REAL):
            prop_type = "REAL"
            prop_value = c_value.value
        else:
            prop_type = "NONE"
            prop_value = False

        return [prop_value, prop_type]

    def isCameraProperty(self, property_name, camera_id):
        """
        Check if a property name is supported by the camera.
        """
        properties = self.camera[camera_id].properties
        print(properties)
        if property_name in properties:
            return True
        else:
            return False

    def setPropertyValue(self, property_name, property_value, camera_id):
        """
        Set the value of a property.
        """
        handle = self.camera[camera_id].handle
        properties = self.camera[camera_id].properties

        # Check if the property exists.
        if not (property_name in properties):
            print(" unknown property name:", property_name)
            return False

        # If the value is text, figure out what the
        # corresponding numerical property value is.
        if (isinstance(property_value, str)):
            text_values = self.getPropertyText(property_name, camera_id)
            if (property_value in text_values):
                property_value = float(text_values[property_value])
            else:
                print(" unknown property text value:", property_value, "for", property_name)
                return False

        # Check that the property is within range.
        [pv_min, pv_max] = self.getPropertyRange(property_name, camera_id)
        if (property_value < pv_min):
            print(" set property value", property_value, "is less than minimum of", pv_min, property_name,
                  "setting to minimum")
            property_value = pv_min
        if (property_value > pv_max):
            print(" set property value", property_value, "is greater than maximum of", pv_max, property_name,
                  "setting to maximum")
            property_value = pv_max

        # Set the property value, return what it was set too.
        prop_id = properties[property_name]
        p_value = ctypes.c_double(property_value)
        self.checkStatus(self._dcam.dcamprop_setgetvalue(handle,
                                                         ctypes.c_int32(prop_id),
                                                         ctypes.byref(p_value),
                                                         ctypes.c_int32(DCAM_DEFAULT_ARG)),
                         "dcamprop_setgetvalue", camera_id)

        return p_value.value

    def sortedPropertyTextOptions(self, property_name, camera_id):
        """
        Returns the property text options a list sorted by value.
        """
        text_values = self.getPropertyText(property_name, camera_id)
        return sorted(text_values, key=text_values.get)

    def getCameraProperties(self, camera_id):
        """
        Return the ids & names of all the properties that the camera supports. This
        is used at initialization to populate the self.properties attribute.
        """
        handle = self.camera[camera_id].handle

        c_buf_len = 64
        c_buf = ctypes.create_string_buffer(c_buf_len)
        properties = {}
        prop_id = ctypes.c_int32(0)

        # Reset to the start
        ret = self._dcam.dcamprop_getnextid(handle, ctypes.byref(prop_id), ctypes.c_uint32(DCAMPROP_OPTION_NEAREST))
        if (ret != 0) and (ret != DCAMERR_NOERROR):
            self.checkStatus(ret, "dcamprop_getnextid", camera_id)

        # Get the first property.
        ret = self._dcam.dcamprop_getnextid(handle, ctypes.byref(prop_id), ctypes.c_int32(DCAMPROP_OPTION_NEXT))
        if (ret != 0) and (ret != DCAMERR_NOERROR):
            self.checkStatus(ret, "dcamprop_getnextid", camera_id)
        self.checkStatus(self._dcam.dcamprop_getname(handle, prop_id, c_buf, ctypes.c_int32(c_buf_len)),
                         "dcamprop_getname", camera_id)

        # Get the rest of the properties.
        last = -1
        while prop_id.value != last:
            last = prop_id.value
            properties[convertPropertyName(c_buf.value.decode(self.encoding))] = prop_id.value
            ret = self._dcam.dcamprop_getnextid(handle, ctypes.byref(prop_id), ctypes.c_int32(DCAMPROP_OPTION_NEXT))
            if (ret != 0) and (ret != DCAMERR_NOERROR):
                self.checkStatus(ret, "dcamprop_getnextid", camera_id)
            self.checkStatus(self._dcam.dcamprop_getname(handle, prop_id, c_buf, ctypes.c_int32(c_buf_len)),
                             "dcamprop_getname", camera_id)

        return properties

    @staticmethod
    def addMissingProperties(properties):
        # manually add missing properties (arrays)
        properties["output_trigger_active[1]"] = int(properties["output_trigger_active[0]"]) + 256
        properties["output_trigger_active[2]"] = int(properties["output_trigger_active[0]"]) + 512
        properties["output_trigger_delay[1]"] = int(properties["output_trigger_delay[0]"]) + 256
        properties["output_trigger_delay[2]"] = int(properties["output_trigger_delay[0]"]) + 512
        properties["output_trigger_kind[1]"] = int(properties["output_trigger_kind[0]"]) + 256
        properties["output_trigger_kind[2]"] = int(properties["output_trigger_kind[0]"]) + 512
        properties["output_trigger_period[1]"] = int(properties["output_trigger_period[0]"]) + 256
        properties["output_trigger_period[2]"] = int(properties["output_trigger_period[0]"]) + 512
        properties["output_trigger_polarity[1]"] = int(properties["output_trigger_polarity[0]"]) + 256
        properties["output_trigger_polarity[2]"] = int(properties["output_trigger_polarity[0]"]) + 512
        properties["output_trigger_source[1]"] = int(properties["output_trigger_source[0]"]) + 256
        properties["output_trigger_source[2]"] = int(properties["output_trigger_source[0]"]) + 512

    def showCameraInfo(self, camera_id):
        print("  manufacturer:", self.getCameraManufacturer(camera_id))
        print("  model:", self.getCameraModel(camera_id))
        print("  version:", self.getCameraVersion(camera_id))
        print("  driver version:", self.getCameraDriverVersion(camera_id))
        print("  module version:", self.getCameraModuleVersion(camera_id))
        print("  API version:", self.getCameraAPIVersion(camera_id))
        print("\n")

    def getCameraManufacturer(self, camera_id):
        """
        Camera Model Name. The model number of the device, e.g. "C11440-22C".
        Some device may have additional options. Those options are described
        in this string after "with".
        """

        c_buf_len = 20
        string_value = ctypes.create_string_buffer(c_buf_len)
        paramstring = DCAMDEV_STRING(
            0,
            DCAM_IDSTR_VENDOR,
            ctypes.cast(string_value, ctypes.c_char_p),
            c_buf_len)
        paramstring.size = ctypes.sizeof(paramstring)

        self.checkStatus(self._dcam.dcamdev_getstring(ctypes.c_int32(camera_id), ctypes.byref(paramstring)),
                         "dcamdev_getstring", camera_id)

        return string_value.value.decode(self.encoding)

    def getCameraModel(self, camera_id):
        """
        Camera Model Name. The model number of the device, e.g. "C11440-22C".
        Some device may have additional options. Those options are described
        in this string after "with".
        """

        c_buf_len = 20
        string_value = ctypes.create_string_buffer(c_buf_len)
        paramstring = DCAMDEV_STRING(
            0,
            DCAM_IDSTR_MODEL,
            ctypes.cast(string_value, ctypes.c_char_p),
            c_buf_len)
        paramstring.size = ctypes.sizeof(paramstring)

        self.checkStatus(self._dcam.dcamdev_getstring(ctypes.c_int32(camera_id), ctypes.byref(paramstring)),
                         "dcamdev_getstring", camera_id)

        return string_value.value.decode(self.encoding)

    def getCameraVersion(self, camera_id):
        """
        Camera version. This value will represent the
        version of the firmware and/or hardware
        """

        c_buf_len = 20
        string_value = ctypes.create_string_buffer(c_buf_len)
        paramstring = DCAMDEV_STRING(
            0,
            DCAM_IDSTR_CAMERAVERSION,
            ctypes.cast(string_value, ctypes.c_char_p),
            c_buf_len)
        paramstring.size = ctypes.sizeof(paramstring)

        self.checkStatus(self._dcam.dcamdev_getstring(ctypes.c_int32(camera_id), ctypes.byref(paramstring)),
                         "dcamdev_getstring", camera_id)

        return string_value.value.decode(self.encoding)

    def getCameraDriverVersion(self, camera_id):
        """
        Driver Version. This is the version of the lower level driver
        which DCAM is using for this device. This value can represent
        the kernel driver and/or shared library.
        """
        c_buf_len = 20
        string_value = ctypes.create_string_buffer(c_buf_len)
        paramstring = DCAMDEV_STRING(
            0,
            DCAM_IDSTR_DRIVERVERSION,
            ctypes.cast(string_value, ctypes.c_char_p),
            c_buf_len)
        paramstring.size = ctypes.sizeof(paramstring)

        self.checkStatus(self._dcam.dcamdev_getstring(ctypes.c_int32(camera_id), ctypes.byref(paramstring)),
                         "dcamdev_getstring", camera_id)

        return string_value.value.decode(self.encoding)

    def getCameraModuleVersion(self, camera_id):
        """
        Module Version. This is the version of the DCAM module.
        """
        c_buf_len = 20
        string_value = ctypes.create_string_buffer(c_buf_len)
        paramstring = DCAMDEV_STRING(
            0,
            DCAM_IDSTR_MODULEVERSION,
            ctypes.cast(string_value, ctypes.c_char_p),
            c_buf_len)
        paramstring.size = ctypes.sizeof(paramstring)

        self.checkStatus(self._dcam.dcamdev_getstring(ctypes.c_int32(camera_id), ctypes.byref(paramstring)),
                         "dcamdev_getstring", camera_id)

        return string_value.value.decode(self.encoding)

    def getCameraAPIVersion(self, camera_id):
        """
        DCAM-API Version. This is the version of DCAM-API specification.
        For example, if this is "4.0", it means the device can run with
        DCAM-API v4.0 specification.
        """
        c_buf_len = 20
        string_value = ctypes.create_string_buffer(c_buf_len)
        paramstring = DCAMDEV_STRING(
            0,
            DCAM_IDSTR_DCAMAPIVERSION,
            ctypes.cast(string_value, ctypes.c_char_p),
            c_buf_len)
        paramstring.size = ctypes.sizeof(paramstring)

        self.checkStatus(self._dcam.dcamdev_getstring(ctypes.c_int32(camera_id), ctypes.byref(paramstring)),
                         "dcamdev_getstring", camera_id)

        return string_value.value.decode(self.encoding)

    def setSubArrayMode(self, camera_id):
        """
        This sets the sub-array mode as appropriate based on the current ROI.
        """

        # Check ROI properties.
        roi_w = self.getPropertyValue("subarray_hsize", camera_id)[0]
        roi_h = self.getPropertyValue("subarray_vsize", camera_id)[0]

        # If the ROI is smaller than the entire frame turn on subarray mode
        if (roi_w == self.camera[camera_id].max_width) and (roi_h == self.camera[camera_id].max_height):
            self.setPropertyValue("subarray_mode", 1, camera_id)
        else:
            self.setPropertyValue("subarray_mode", 2, camera_id)

    def setACQMode(self, mode, number_frames=None, camera_id=0):
        """
        Set the acquisition mode to either run until aborted or to
        stop after acquiring a set number of frames.

        mode should be either "fixed_length" or "run_till_abort"

        if mode is "fixed_length", then number_frames indicates the number
        of frames to acquire.
        """

        self.stopAcquisition(camera_id)

        if self.camera[camera_id].acquisition_mode == "fixed_length" or self.camera[camera_id].acquisition_mode == "run_till_abort":
            self.camera[camera_id].acquisition_mode = mode
            self.camera[camera_id].number_frames = number_frames
        else:
            raise DCAMException("Unrecognized acquisition mode: " + mode)

    def captureSetup(self, camera_id):
        """
        Capture setup (internal use only). This is called at the start
        of new acquisition sequence to determine the current ROI and
        get the camera configured properly.
        """
        self.camera[camera_id].buffer_index = -1
        self.camera[camera_id].last_frame_number = 0

        # Set sub array mode.
        self.setSubArrayMode(camera_id)

        # Get frame properties.
        self.camera[camera_id].frame_x = self.getPropertyValue("image_width", camera_id)[0]
        self.camera[camera_id].frame_y = self.getPropertyValue("image_height", camera_id)[0]
        self.camera[camera_id].frame_bytes = self.getPropertyValue("image_framebytes", camera_id)[0]

    def startAcquisition(self, camera_id):
        """
        Start data acquisition.
        """
        self.captureSetup(camera_id)
        handle = self.camera[camera_id].handle

        #
        # Allocate Hamamatsu image buffers.
        # We allocate enough to buffer 2 seconds of data or the specified
        # number of frames for a fixed length acquisition
        #
        n_buffers = 0
        if self.camera[camera_id].acquisition_mode == "run_till_abort":
            n_buffers = self.camera[camera_id].number_frames
        elif self.camera[camera_id].acquisition_mode == "fixed_length":
            n_buffers = self.camera[camera_id].number_frames
        self.camera[camera_id].number_image_buffers = n_buffers

        self.checkStatus(self._dcam.dcambuf_alloc(handle, ctypes.c_int32(self.camera[camera_id].number_image_buffers)),
                         "dcambuf_alloc", camera_id)

        # Start acquisition.
        if self.camera[camera_id].acquisition_mode == "run_till_abort":
            self.checkStatus(self._dcam.dcamcap_start(handle, DCAMCAP_START_SEQUENCE),
                             "dcamcap_start", camera_id)
        if self.camera[camera_id].acquisition_mode == "fixed_length":
            self.checkStatus(self._dcam.dcamcap_start(handle, DCAMCAP_START_SNAP),
                             "dcamcap_start", camera_id)

    def stopAcquisition(self, camera_id):
        """
        Stop data acquisition.
        """
        handle = self.camera[camera_id].handle

        # Stop acquisition.
        self.checkStatus(self._dcam.dcamcap_stop(handle),
                         "dcamcap_stop", camera_id)

        # print("max camera {} backlog was {} of {}".format(camera_id,
        #                                                   self.camera[camera_id].max_backlog,
        #                                                   self.camera[camera_id].number_image_buffers))
        self.camera[camera_id].max_backlog = 0

    def newFrames(self, camera_id):
        """
        Return a list of the ids of all the new frames since the last check.
        Returns an empty list if the camera has already stopped and no frames
        are available.

        This will block waiting for at least one new frame.
        """
        handle = self.camera[camera_id].handle
        wait_handle = self.camera[camera_id].wait_handle

        captureStatus = ctypes.c_int32(0)
        self.checkStatus(self._dcam.dcamcap_status(handle, ctypes.byref(captureStatus)),
                         "dcamcap_status", camera_id)

        # Wait for a new frame if the camera is acquiring.
        if captureStatus.value == DCAMCAP_STATUS_BUSY:
            paramstart = DCAMWAIT_START(
                0,
                0,
                DCAMWAIT_CAPEVENT_FRAMEREADY | DCAMWAIT_CAPEVENT_STOPPED,
                DCAMWAIT_TIMEOUT_INFINITE)
            paramstart.size = ctypes.sizeof(paramstart)
            self.checkStatus(self._dcam.dcamwait_start(wait_handle, ctypes.byref(paramstart)),
                             "dcamwait_start", camera_id)

        # Check how many new frames there are.
        paramtransfer = DCAMCAP_TRANSFERINFO(0, DCAMCAP_TRANSFERKIND_FRAME, 0, 0)
        paramtransfer.size = ctypes.sizeof(paramtransfer)
        self.checkStatus(self._dcam.dcamcap_transferinfo(handle, ctypes.byref(paramtransfer)),
                         "dcamcap_transferinfo", camera_id)
        cur_buffer_index = paramtransfer.nNewestFrameIndex
        cur_frame_number = paramtransfer.nFrameCount

        self.camera[camera_id].ctrl_buff_index = cur_buffer_index
        self.camera[camera_id].ctrl_frame_number = cur_frame_number

        # Check that we have not acquired more frames than we can store in our buffer.
        # Keep track of the maximum backlog.
        backlog = cur_frame_number - self.camera[camera_id].last_frame_number
        if backlog > self.camera[camera_id].number_image_buffers:
            raise MemoryError(">>> Hamamatsu camera frame buffer overrun detected! <<<")
        if backlog > self.camera[camera_id].max_backlog:
            self.camera[camera_id].max_backlog = backlog
        self.camera[camera_id].last_frame_number = cur_frame_number

        # Create a list of the new frames.
        new_frames = []
        if (cur_buffer_index < self.camera[camera_id].buffer_index):
            for i in range(self.camera[camera_id].buffer_index + 1, self.camera[camera_id].number_image_buffers):
                new_frames.append(i)
            for i in range(cur_buffer_index + 1):
                new_frames.append(i)
        else:
            for i in range(self.camera[camera_id].buffer_index, cur_buffer_index):
                new_frames.append(i + 1)
        self.camera[camera_id].buffer_index = cur_buffer_index

        # print("Found {} frames (in newFrames)".format(len(new_frames)))
        return new_frames

    def getFrames(self, camera_id):
        """
        Gets all of the available frames.

        This will block waiting for new frames even if
        there are new frames available when it is called.
        """
        handle = self.camera[camera_id].handle

        frames = []
        timestamps = []
        for n in self.newFrames(camera_id):
            paramtime = DCAM_TIMESTAMP(0, 0)
            paramlock = DCAMBUF_FRAME(
                0, 0, 0, n, None, 0, 0, 0, 0, 0, 0, paramtime, 0, 0)
            paramlock.size = ctypes.sizeof(paramlock)

            # Lock the frame in the camera buffer & get address.
            self.checkStatus(self._dcam.dcambuf_lockframe(handle, ctypes.byref(paramlock)), "dcambuf_lockframe", camera_id)

            # Create storage for the frame & copy into this storage.
            hc_data = HCamData(self.camera[camera_id].frame_bytes)
            hc_data.copyData(paramlock.buf)

            frames.append(hc_data)
            stamp = [paramlock.camerastamp,
                     paramlock.framestamp,
                     paramlock.timestamp.sec + paramlock.timestamp.microsec / 1e6]
            timestamps.append(stamp)

        return [frames, timestamps, [self.camera[camera_id].frame_x, self.camera[camera_id].frame_y]]
    
    def prepare_for_acquisition(self, config):
        self.config = config

        for camera_id in self.config.camera.get_active_cameras_ids():
            camera_props = self.config.camera[camera_id].props
            for prop in camera_props:
                key = prop.key
                value = prop.value
                self.setPropertyValue(key, value, camera_id)
                # time.sleep(0.01)

            assert int(self.config.camera[camera_id].subarray_hpos.value) == int(self.getPropertyValue("subarray_hpos", camera_id)[0])
            assert int(self.config.camera[camera_id].subarray_hsize.value) == int(self.getPropertyValue("subarray_hsize", camera_id)[0])
            assert int(self.config.camera[camera_id].subarray_vpos.value) == int(self.getPropertyValue("subarray_vpos", camera_id)[0])
            assert int(self.config.camera[camera_id].subarray_vsize.value) == int(self.getPropertyValue("subarray_vsize", camera_id)[0])


    def acquire(self, metadata, preprocessing_queue):
        # assert settings were applied to camera
        assert self.config is not None

        active_camera_ids = self.config.ACTIVE_CAMERA_IDS
        num_active_cameras = self.config.NUM_ACTIVE_CAMERAS
        num_timepoints = self.config.SIZE_T
        num_preprocessing_workers = self.config.NUM_PREPROCESS_WORKERS

        num_data_buffers = len(self.data_buffers)
        size_z = len(self.data_buffers[0][0])
        num_channels_per_camera = self.config.NUM_ACTIVE_CHANNELS_PER_CAMERA  # WHAT THE FUCK IS ACTIVE CHANNEL ???
        num_images_per_volume_per_camera = [x * size_z for x in num_channels_per_camera]
        tot_num_images = [x * num_timepoints for x in num_images_per_volume_per_camera]

        cnts = [0 for _ in range(num_active_cameras)]
        while True:
            if sum(cnts) == sum(tot_num_images):
                return
            for i, camera_id in enumerate(active_camera_ids):
                j = int((i+1) % 2)

                handle = self.camera[camera_id].handle  # pointer to handle
                size = self.camera[camera_id].frame_bytes

                new_frames = self.newFrames(camera_id)
                for n in new_frames:
                    # get coordinates of current frame
                    t = int(cnts[i] // (num_channels_per_camera[i] * size_z))
                    z = int((cnts[i] % num_images_per_volume_per_camera[i]) // num_channels_per_camera[i])
                    c = self.config.camera[camera_id].channels[int(cnts[i] % num_channels_per_camera[i])].c_in_buf
                    # c = active_channels[i][int(cnts[i] % num_channels_per_camera[i])]["channel_id"]  # order in BGRY order for later simplicity
                    
                    buffer_id = int(t % num_data_buffers)

                    with self.locks[buffer_id]:  # acquire lock for buffer_id
                        cnt_end_volume = [int(x * (t + 1)) for x in num_images_per_volume_per_camera]

                        paramtime = DCAM_TIMESTAMP(0, 0)
                        paramlock = DCAMBUF_FRAME(0, 0, 0, n, None, 0, 0, 0, 0, 0, 0, paramtime, 0, 0)
                        paramlock.size = ctypes.sizeof(paramlock)

                        # Lock the frame in the camera buffer & get address.
                        self.checkStatus(self._dcam.dcambuf_lockframe(handle, ctypes.byref(paramlock)), "dcambuf_lockframe", camera_id)

                        # Create storage for the frame & copy into this storage.
                        ctypes.memmove(ctypes.addressof(self.data_buffers[buffer_id][c][z]), paramlock.buf, size)
                        stamp = [paramlock.camerastamp, paramlock.framestamp, paramlock.timestamp.sec + paramlock.timestamp.microsec / 1e6]
                        metadata[sum(cnts)] = numpy.asarray([camera_id, cnts[i], t, c, z] + stamp)

                    # print("camera={}, image={}, camera_stamp={}, framestamp={} t={}, z={}, c={}, cnts={}".format(camera_id, n, stamp[0], stamp[1], t, z, c, cnts))
                    # assert int(stamp[1]) == int(cnts[i]) % 2**16  # assert no frames were lost, camera counter is 16 bits
                    cnts[i] += 1

                    if num_active_cameras == 2:
                        if (cnts[i] == cnt_end_volume[i]) and (cnts[j] >= cnt_end_volume[j]):
                            print("Finished acquisition of volume {} / {}".format(t, num_timepoints))
                            preprocessing_queue.put((buffer_id, t))  # (camera_id, buffer_id, time)
                        if sum(cnts) == sum(tot_num_images):
                            for _ in range(num_preprocessing_workers):
                                preprocessing_queue.put((None, None))
                            return None
                    elif num_active_cameras == 1:
                        if cnts[i] == cnt_end_volume[i]:
                            print("Finished acquisition of volume {} / {}".format(t, num_timepoints))
                            preprocessing_queue.put((buffer_id, t))  # (camera_id, buffer_id, time)
                        if sum(cnts) == sum(tot_num_images):
                            for _ in range(num_preprocessing_workers):
                                preprocessing_queue.put((None, None))
                            return None

    def closeCamera(self, camera_id):
        wait_handle = self.camera[camera_id].wait_handle
        handle = self.camera[camera_id].handle
        self.checkStatus(self._dcam.dcamwait_close(wait_handle), "dcamwait_close", camera_id)
        self.checkStatus(self._dcam.dcamdev_close(handle), "dcamdev_close", camera_id)

    def close(self):
        """
        Close down the connection to the camera.
        """
        self.closeCamera(0)
        self.closeCamera(1)
        print("uniniting api...")
        self.checkStatus(self._dcam.dcamapi_uninit(), "dcamapi_uninit")
        print("done uniniting api...")

    def checkStatus(self, fn_return, fn_name="unknown", camera_id=0):
        """
        Check return value of the dcam function call.
        Throw an error if not as expected?
        """
        try:
            handle = self.camera[camera_id].handle
        except:
            pass

        # if (fn_return != DCAMERR_NOERROR) and (fn_return != DCAMERR_ERROR):
        #    raise DCAMException("dcam error: " + fn_name + " returned " + str(fn_return))
        if (fn_return == DCAMERR_ERROR):
            c_buf_len = 80
            c_buf = ctypes.create_string_buffer(c_buf_len)
            c_error = self._dcam.dcam_getlasterror(handle, c_buf, ctypes.c_int32(c_buf_len))
            raise DCAMException("dcam error " + str(fn_name) + " " + str(c_buf.value))
            # print "dcam error", fn_name, c_buf.value
        return fn_return


###########
# Testing.#
###########

if __name__ == "__main__":

    import time
    import random
    
    camera_id = 0

    hcam = HamamatsuCamera()
    
    print(hcam.setPropertyValue("defect_correct_mode", 1, camera_id))

    # List support properties.
    if False:
        print("Supported properties:")
        props = hcam.getProperties(camera_id)
        for i, id_name in enumerate(sorted(props.keys())):
            [p_value, p_type] = hcam.getPropertyValue(id_name, camera_id)
            # p_rw = hcam.getPropertyRW(id_name, camera_id)
            p_rw = [True,True] #modifié ici !
            read_write = ""
            if (p_rw[0]):
                read_write += "read"
            if (p_rw[1]):
                read_write += ", write"
            print("  ", i, ")", id_name, " = ", p_value, " type is:", p_type, ",", read_write)
            text_values = hcam.getPropertyText(id_name, camera_id)
            if (len(text_values) > 0):
                print("          option / value")
                for key in sorted(text_values, key=text_values.get):
                    print("         ", key, "/", text_values[key])

    # Test setting & getting some parameters.
    if False:
        print(hcam.setPropertyValue("exposure_time", 0.001, camera_id))
        print(hcam.setPropertyValue("subarray_hpos", 512, camera_id))
        print(hcam.setPropertyValue("subarray_vpos", 512, camera_id))
        print(hcam.setPropertyValue("subarray_hsize", 1024, camera_id))
        print(hcam.setPropertyValue("subarray_vsize", 1024, camera_id))

        print(hcam.setPropertyValue("binning", "1x1", camera_id))
        print(hcam.setPropertyValue("readout_speed", 2, camera_id))

        hcam.setSubArrayMode(camera_id)
        # hcam.startAcquisition()
        # hcam.stopAcquisition()

        params = ["internal_frame_rate",
                  "timing_readout_time",
                  "exposure_time"]

        #                      "image_height",
        #                      "image_width",
        #                      "image_framebytes",
        #                      "buffer_framebytes",
        #                      "buffer_rowbytes",
        #                      "buffer_top_offset_bytes",
        #                      "subarray_hsize",
        #                      "subarray_vsize",
        #                      "binning"]
        for param in params:
            print(param, hcam.getPropertyValue(param,camera_id)[0])

    # Test 'run_till_abort' acquisition.
    if False:
        print("Testing run till abort acquisition")
        hcam.setACQMode("run_till_abort",600,camera_id)
        hcam.startAcquisition(camera_id)
        cnt = 0
        for i in range(300):
            [frames, dims, size] = hcam.getFrames(camera_id)
            for aframe in frames:
                print(cnt, aframe[0:5])
                cnt += 1

        print("Frames acquired: " + str(cnt))
        hcam.stopAcquisition(camera_id)

    # Test 'fixed_length' acquisition.
    if False:
        for j in range(1):
            print("Testing fixed length acquisition")
            hcam.setACQMode("fixed_length", 10, camera_id)
            hcam.startAcquisition(camera_id)
            cnt = 0
            iterations = 0
            while cnt < 11 and iterations < 11:
                [frames, dims, size] = hcam.getFrames(camera_id)
                waitTime = random.random() * 0.03
                time.sleep(waitTime)
                iterations += 1
                print('Frames loaded: ' + str(len(frames)))
                print('Wait time: ' + str(waitTime))
                for aframe in frames:
                    print(cnt, aframe[0:5])
                    cnt += 1
                    
                    
            if cnt < 10:
                print('##############Error: Not all frames found#########')
                input("Press enter to continue")
            print("Frames acquired: " + str(cnt))
            hcam.stopAcquisition(camera_id)

#
# The MIT License
#
# Copyright (c) 2013 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
