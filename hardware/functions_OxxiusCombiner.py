# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 11:47:17 2025

@author: tbrugiere
"""

import serial
import time

class OxxiusCombiner:
    """
    Pilote Oxxius L4Cc / L6Cc en USB (port série virtuel).
    - model: "L4Cc" ou "L6Cc"
    - baudrate: souvent 115200 sur l'USB-CDC du combiner (modifier si besoin)
    """
    def __init__(self, port, model="L4Cc", baudrate=115200, timeout=0.5):
        model = model.strip().upper()
        if model not in ("L4CC", "L6CC"):
            raise ValueError("model doit être 'L4Cc' ou 'L6Cc'")
        self.model = model
        self.max_channels = 4 if model == "L4CC" else 6

        self.ser = serial.Serial(
            port=port, baudrate=baudrate,
            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE, timeout=timeout
        )
        time.sleep(0.2)

    # ---------- bas niveau ----------
    def _chk_ch(self, ch):
        if not (1 <= ch <= self.max_channels):
            raise ValueError(f"Canal invalide (1..{self.max_channels})")
        return ch

    def _send(self, ch, cmd):
        """Envoie 'L<ch> <cmd>\\n' et retourne la ligne de réponse (str, sans \\r\\n)."""
        self._chk_ch(ch)
        line = f"L{ch} {cmd}\n"
        self.ser.write(line.encode("ascii"))
        resp = self.ser.readline().decode("ascii", errors="ignore").strip()
        return resp

    def close(self):
        try:
            self.ser.close()
        except Exception:
            pass

    # ---------- helpers typiques ----------
    # Puissance absolue (mW)
    def set_power_mw(self, ch: int, mw: float):
        """Règle la puissance en mW (p.ex. 10.5)."""
        return self._send(ch, f"PL1 {mw}")

    # Puissance relative (% du nominal)
    def set_power_percent(self, ch: int, pct: float):
        """Règle la puissance en % du nominal (p.ex. 25.0)."""
        return self._send(ch, f"PPL1 {pct}")

    # Lecture puissance mesurée (mW)
    def read_power_mw(self, ch: int):
        """Retourne la mesure optique en mW si disponible."""
        resp = self._send(ch, "?P")
        try:
            return float(resp)
        except ValueError:
            return resp  # renvoyer brut si ce n'est pas un nombre

    # Boucle de régulation (APC = puissance, ACC = courant)
    def set_loop_apc(self, ch: int, enable=True):
        return self._send(ch, f"APC {1 if enable else 0}")

    def set_loop_acc(self, ch: int, enable=True):
        return self._send(ch, f"ACC {1 if enable else 0}")

    # Modulation analogique (AM)
    def set_analog_mod(self, ch: int, enable: bool):
        """Active/désactive l'entrée analogique de modulation."""
        return self._send(ch, f"AM {1 if enable else 0}")

    # Modulation digitale (TTL)
    def set_digital_mod(self, ch: int, enable: bool):
        """
        Active/désactive la modulation digitale.
        Selon firmware, la commande peut être CW ou DM.
        - Sur têtes LBX: CW 0 = enable, CW 1 = disable (logique inversée)
        - Sur combiner: DM 1/0 peut être présent. On tente CW puis DM si erreur.
        """
        # Essai 1: CW (logique LBX: 0=enable, 1=disable)
        resp = self._send(ch, f"CW {0 if enable else 1}")
        if resp.upper().startswith("ERR"):
            # Essai 2: DM (logique directe 1=enable, 0=disable)
            resp = self._send(ch, f"DM {1 if enable else 0}")
        return resp

    # Shutter de la voie (si présent)
    def set_shutter(self, ch: int, open_: bool):
        """Ouvre/ferme le shutter de la voie."""
        return self._send(ch, f"SH1 {1 if open_ else 0}")

    # Statuts utiles
    def get_status(self, ch: int):
        return self._send(ch, "?STA")

    def get_emission_state(self, ch: int):
        """État émission (peut renvoyer 0/1 ou un texte selon firmware)."""
        return self._send(ch, "?L")

    # Pass-through générique
    def send_raw(self, ch: int, cmd: str):
        return self._send(ch, cmd)


# ------------- Exemple d'utilisation -------------
