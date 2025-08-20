# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 14:28:24 2025

@author: tbrugiere

code généré automatiquement par ChatGPT
"""

import time
import random
from typing import Dict, Any

class MockOxxiusCombiner:
    """
    Simulateur (mock) d'un Oxxius L4Cc / L6Cc pour le développement sans matériel.
    API compatible avec OxxiusCombiner:
      - set_power_mw(ch, mw)
      - set_power_percent(ch, pct)
      - read_power_mw(ch)
      - set_loop_apc(ch, enable)
      - set_loop_acc(ch, enable)
      - set_analog_mod(ch, enable)
      - set_digital_mod(ch, enable)
      - set_shutter(ch, open_)
      - get_status(ch)
      - get_emission_state(ch)
      - send_raw(ch, cmd)
      - close()
    """

    def __init__(self, port="MOCK", model="L4Cc", baudrate=115200, timeout=0.5,
                 simulate_latency_s: float = 0.005, noise_std_mw: float = 0.05,
                 wavelengths_nm: Dict[int, int] = None,
                 nominal_power_mw: Dict[int, float] = None):
        model_u = model.strip().upper()
        if model_u not in ("L4CC", "L6CC"):
            raise ValueError("model doit être 'L4Cc' ou 'L6Cc'")
        self.model = model_u
        self.max_channels = 4 if model_u == "L4CC" else 6
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.simulate_latency_s = simulate_latency_s
        self.noise_std_mw = noise_std_mw

        # Valeurs par défaut (peu importe, c'est un mock)
        if wavelengths_nm is None:
            wavelengths_nm = {i: wl for i, wl in enumerate([405, 445, 488, 561, 637, 730], start=1)}
        if nominal_power_mw is None:
            nominal_power_mw = {i: p for i, p in enumerate([50, 60, 100, 100, 140, 80], start=1)}

        # État par canal
        self.state: Dict[int, Dict[str, Any]] = {}
        for ch in range(1, self.max_channels + 1):
            self.state[ch] = {
                "present": ch in wavelengths_nm,
                "wl_nm": wavelengths_nm.get(ch, None),
                "nominal_mw": float(nominal_power_mw.get(ch, 100.0)),
                "setpoint_mw": 0.0,       # cible (PL1)
                "loop_apc": True,         # puissance
                "loop_acc": False,        # courant (exclusif avec apc)
                "am_enabled": False,      # modulation analogique
                "ttl_enabled": False,     # modulation digitale
                "shutter_open": False,    # SH1
                "emission_on": True,      # ?L (on reste simple pour un mock)
                "fault": False,           # pour simuler une erreur
            }

    # ------ utilitaires internes ------
    def _sleep(self):
        if self.simulate_latency_s:
            time.sleep(self.simulate_latency_s)

    def _chk_ch(self, ch: int):
        if not (1 <= ch <= self.max_channels):
            raise ValueError(f"Canal invalide (1..{self.max_channels})")
        if not self.state[ch]["present"]:
            # comme un canal absent => renvoyer une erreur type firmware
            raise RuntimeError("ERR:CH_NOT_PRESENT")

    def _ok(self): return "OK"

    # Puissance effectivement délivrée (simulation)
    def _effective_power_mw(self, ch: int) -> float:
        s = self.state[ch]
        if s["fault"] or not s["emission_on"] or not s["shutter_open"]:
            return 0.0
        # Si TTL est "activée" côté interface, on considère que la porte est ouverte (mock),
        # sinon, si la TTL n'est pas activée, on sort la puissance continue.
        gate = True  # porte virtuelle toujours haute dans le mock
        if not gate:
            return 0.0
        return max(0.0, min(s["setpoint_mw"], s["nominal_mw"]))

    # ------ API publique (même interface que la vraie classe) ------
    def close(self):  # pour compatibilité
        return

    def _send(self, ch: int, cmd: str) -> str:
        """Émule 'L<ch> <cmd>' et retourne une réponse texte."""
        self._chk_ch(ch)
        self._sleep()
        # Parsing minimal des commandes fréquentes
        parts = cmd.strip().split()
        if not parts:
            return "ERR:EMPTY"

        # Interrogations
        if parts[0].upper() in ("?P",):
            p = self._effective_power_mw(ch)
            p_meas = p + random.gauss(0.0, self.noise_std_mw)
            return f"{max(0.0, p_meas):.3f}"
        if parts[0].upper() in ("?STA",):
            s = self.state[ch]
            return f"WL={s['wl_nm']}nm;NOM={s['nominal_mw']:.1f}mW;AM={int(s['am_enabled'])};TTL={int(s['ttl_enabled'])};SH={int(s['shutter_open'])};APC={int(s['loop_apc'])};ACC={int(s['loop_acc'])};FAULT={int(s['fault'])}"
        if parts[0].upper() in ("?L",):
            return "1" if self.state[ch]["emission_on"] else "0"

        # Réglages
        # PL1 <mW>
        if parts[0].upper() == "PL1" and len(parts) >= 2:
            try:
                mw = float(parts[1])
            except ValueError:
                return "ERR:ARG"
            nom = self.state[ch]["nominal_mw"]
            if mw < 0 or mw > 1.20 * nom:
                return "ERR:OUT_OF_RANGE"
            self.state[ch]["setpoint_mw"] = mw
            return self._ok()

        # PPL1 <pct>
        if parts[0].upper() == "PPL1" and len(parts) >= 2:
            try:
                pct = float(parts[1])
            except ValueError:
                return "ERR:ARG"
            if pct < 0 or pct > 120:
                return "ERR:OUT_OF_RANGE"
            self.state[ch]["setpoint_mw"] = self.state[ch]["nominal_mw"] * (pct / 100.0)
            return self._ok()

        # AM 0/1
        if parts[0].upper() == "AM" and len(parts) >= 2:
            val = parts[1]
            if val not in ("0", "1"):
                return "ERR:ARG"
            self.state[ch]["am_enabled"] = (val == "1")
            return self._ok()

        # CW 0/1 (logique LBX: 0=enable, 1=disable)
        if parts[0].upper() == "CW" and len(parts) >= 2:
            val = parts[1]
            if val not in ("0", "1"):
                return "ERR:ARG"
            self.state[ch]["ttl_enabled"] = (val == "0")
            return self._ok()

        # DM 0/1 (alternative)
        if parts[0].upper() == "DM" and len(parts) >= 2:
            val = parts[1]
            if val not in ("0", "1"):
                return "ERR:ARG"
            self.state[ch]["ttl_enabled"] = (val == "1")
            return self._ok()

        # SH1 0/1
        if parts[0].upper() == "SH1" and len(parts) >= 2:
            val = parts[1]
            if val not in ("0", "1"):
                return "ERR:ARG"
            self.state[ch]["shutter_open"] = (val == "1")
            return self._ok()

        # APC / ACC
        if parts[0].upper() in ("APC", "ACC") and len(parts) >= 2:
            val = parts[1]
            if val not in ("0", "1"):
                return "ERR:ARG"
            if parts[0].upper() == "APC":
                self.state[ch]["loop_apc"] = (val == "1")
                self.state[ch]["loop_acc"] = not self.state[ch]["loop_apc"]
            else:
                self.state[ch]["loop_acc"] = (val == "1")
                self.state[ch]["loop_apc"] = not self.state[ch]["loop_acc"]
            return self._ok()

        return "ERR:UNKNOWN_CMD"

    # ----- Helpers identiques à la vraie classe -----
    def set_power_mw(self, ch: int, mw: float):
        return self._send(ch, f"PL1 {mw}")

    def set_power_percent(self, ch: int, pct: float):
        print(f"PPL1 {pct}")
        return self._send(ch, f"PPL1 {pct}")

    def read_power_mw(self, ch: int):
        resp = self._send(ch, "?P")
        try:
            return float(resp)
        except ValueError:
            return resp

    def set_loop_apc(self, ch: int, enable=True):
        return self._send(ch, f"APC {1 if enable else 0}")

    def set_loop_acc(self, ch: int, enable=True):
        return self._send(ch, f"ACC {1 if enable else 0}")

    def set_analog_mod(self, ch: int, enable: bool):
        return self._send(ch, f"AM {1 if enable else 0}")

    def set_digital_mod(self, ch: int, enable: bool):
        # Essaie CW puis DM (comme la vraie classe)
        r = self._send(ch, f"CW {0 if enable else 1}")
        if r.startswith("ERR"):
            r = self._send(ch, f"DM {1 if enable else 0}")
        return r

    def set_shutter(self, ch: int, open_: bool):
        return self._send(ch, f"SH1 {1 if open_ else 0}")

    def get_status(self, ch: int):
        return self._send(ch, "?STA")

    def get_emission_state(self, ch: int):
        return self._send(ch, "?L")

    def send_raw(self, ch: int, cmd: str):
        return self._send(ch, cmd)

    # ----- utilitaires de test -----
    def inject_fault(self, ch: int, fault: bool = True):
        self._chk_ch(ch)
        self.state[ch]["fault"] = fault
        return self._ok()

    def discover(self) -> Dict[int, Dict[str, Any]]:
        """Retourne un petit inventaire des voies présentes."""
        inv = {}
        for ch in range(1, self.max_channels + 1):
            if self.state[ch]["present"]:
                inv[ch] = dict(wl_nm=self.state[ch]["wl_nm"],
                               nominal_mw=self.state[ch]["nominal_mw"])
        return inv