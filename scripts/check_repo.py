#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Contrôles de conventions du dépôt LV8-OS. Sort 0 si tout est conforme, 1 sinon."""

import sys
from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    ".gitattributes",
    ".editorconfig",
]
LICENSE_MARKERS = ["GNU GENERAL PUBLIC LICENSE", "Version 3, 29 June 2007"]
SKIP_DIRS = {".git", "target", "__pycache__", ".venv", "out", "work"}
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".ico", ".iso", ".img", ".qcow2", ".sig", ".gz", ".zst"}
PRIVATE_KEY_MARKER = b"-----BEGIN " + b"PRIVATE KEY-----"  # coupé pour ne pas se détecter lui-même
PRIVATE_KEY_MARKERS = [
    PRIVATE_KEY_MARKER,
    b"-----BEGIN RSA " + b"PRIVATE KEY-----",
    b"-----BEGIN OPENSSH " + b"PRIVATE KEY-----",
    b"-----BEGIN PGP " + b"PRIVATE KEY BLOCK-----",
]


def iter_files(root):
    for path in root.rglob("*"):
        if path.is_file() and not SKIP_DIRS.intersection(path.relative_to(root).parts):
            yield path


def check(root):
    errors = []
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"fichier requis absent : {name}")

    license_file = root / "LICENSE"
    if license_file.is_file():
        head = license_file.read_text(encoding="utf-8", errors="replace")[:500]
        if not all(marker in head for marker in LICENSE_MARKERS):
            errors.append("LICENSE n'est pas le texte GPL-3.0")

    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        if any(marker in data for marker in PRIVATE_KEY_MARKERS):
            errors.append(f"clé privée détectée : {rel}")
        if path.suffix.lower() not in BINARY_SUFFIXES and b"\0" not in data and b"\r\n" in data:
            errors.append(f"fins de ligne CRLF : {rel}")
    return errors


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errors = check(root)
    for error in errors:
        print(f"ERREUR: {error}", file=sys.stderr)
    if not errors:
        print("check_repo: OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
