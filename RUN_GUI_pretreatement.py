# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:07:02 2026

@author: tbrugiere
"""
import os
import subprocess
from pathlib import Path
import sys


ENV_DIR = Path(r"C:\Users\Public\miniconda_envs\OPM_gpu")
ENV_PYTHON = ENV_DIR / "python.exe"
SCRIPT = Path(r"D:\Projets_Python\OPM_GUI\image_analysis\GUI_pretreatement.py")


def main() -> None:
    """Lance le script avec l'interpréteur de l'environnement partagé."""
    if not ENV_PYTHON.is_file():
        raise FileNotFoundError(
            f"Interpréteur introuvable : {ENV_PYTHON}"
        )

    if not SCRIPT.is_file():
        raise FileNotFoundError(
            f"Script introuvable : {SCRIPT}"
        )

    env = os.environ.copy()

    conda_paths = [
        ENV_DIR,
        ENV_DIR / "Library" / "mingw-w64" / "bin",
        ENV_DIR / "Library" / "usr" / "bin",
        ENV_DIR / "Library" / "bin",
        ENV_DIR / "Scripts",
        ENV_DIR / "bin",
    ]

    env["PATH"] = os.pathsep.join(
        [str(path) for path in conda_paths]
        + [env.get("PATH", "")]
    )

    result = subprocess.run(
        [str(ENV_PYTHON), str(SCRIPT)],
        check=False,
        env=env,
        cwd=SCRIPT.parent,
    )

    if result.returncode != 0:
        print(
            f"\nL'application s'est terminée avec le code "
            f"{result.returncode} "
            f"(0x{result.returncode & 0xFFFFFFFF:08X})."
        )
        input("\nAppuyez sur Entrée pour fermer...")

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()