#!/usr/bin/env python3
"""Download public pilot datasets (APTOS via Kaggle, MESSIDOR-2 sample)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def run(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Command failed: {cmd}\n  {e}")
        return False


def download_aptos_kaggle(dest: Path) -> bool:
    dest.mkdir(parents=True, exist_ok=True)
    print("Downloading APTOS 2019 from Kaggle...")
    return run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "kaggle",
            "-q",
        ]
    ) and run(
        [
            "kaggle",
            "competitions",
            "download",
            "-c",
            "aptos2019-blindness-detection",
            "-p",
            str(dest),
        ]
    )


def extract_aptos(dest: Path) -> Path:
    for z in dest.glob("*.zip"):
        print(f"Extracting {z}")
        with zipfile.ZipFile(z, "r") as zf:
            zf.extractall(dest)
    return dest


def download_messidor_sample(dest: Path) -> bool:
    """
    Fetch a small public MESSIDOR-style sample if full dataset unavailable.
    Uses Messidor sample images from a known public mirror when possible.
    """
    dest.mkdir(parents=True, exist_ok=True)
    sample_url = (
        "https://www.adhocdata.org/messidor/Messidor-2.zip"
    )
    zip_path = dest / "Messidor-2.zip"
    if not zip_path.exists():
        print(f"Downloading MESSIDOR-2 from {sample_url} ...")
        try:
            urllib.request.urlretrieve(sample_url, zip_path)
        except Exception as e:
            print(f"MESSIDOR download failed: {e}")
            print("Place MESSIDOR-2 images manually under data/raw/messidor/")
            return False
    if zip_path.exists():
        print(f"Extracting {zip_path}")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(dest)
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aptos-only", action="store_true")
    parser.add_argument("--messidor-only", action="store_true")
    args = parser.parse_args()

    do_aptos = not args.messidor_only
    do_messidor = not args.aptos_only

    aptos_dir = RAW / "aptos"
    messidor_dir = RAW / "messidor"

    if do_aptos:
        if download_aptos_kaggle(aptos_dir):
            extract_aptos(aptos_dir)
        else:
            print("Kaggle download skipped. Configure ~/.kaggle/kaggle.json and retry.")

    if do_messidor:
        download_messidor_sample(messidor_dir)

    prep = ROOT / "scripts" / "prepare_aptos_messidor.py"
    if aptos_dir.exists() and any(aptos_dir.rglob("*.png")) or (aptos_dir / "train.csv").exists():
        run(
            [
                sys.executable,
                str(prep),
                "--aptos-dir",
                str(aptos_dir),
                "--messidor-dir",
                str(messidor_dir),
                "--sample",
                "800",
            ]
        )


if __name__ == "__main__":
    main()
