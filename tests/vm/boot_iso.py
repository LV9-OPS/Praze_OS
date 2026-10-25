#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Démarre l'ISO LV8 dans QEMU et attend l'invite de connexion sur la console série.

Usage : boot_iso.py ISO --firmware bios|uefi [--timeout S] [--log FICHIER]
Sort 0 si l'invite apparaît avant le délai, 1 sinon. La sortie série complète est
écrite dans le journal pour diagnostic.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

MARKER = b"login:"
OVMF_CODE = "/usr/share/OVMF/OVMF_CODE_4M.fd"
OVMF_VARS = "/usr/share/OVMF/OVMF_VARS_4M.fd"


def kvm_available():
    return os.path.exists("/dev/kvm") and os.access("/dev/kvm", os.R_OK | os.W_OK)


def qemu_command(iso, firmware, vars_copy, cpu="host", kvm=None):
    """cpu : modèle QEMU ; 'qemu64' = x86-64 de base sans SSE4/AVX (ADR 0002)."""
    kvm = kvm_available() if kvm is None else kvm
    cmd = [
        "qemu-system-x86_64", "-m", "2048", "-smp", "2",
        "-display", "none", "-serial", "stdio", "-no-reboot",
        "-cdrom", str(iso), "-boot", "d",
    ]
    if kvm:
        cmd += ["-enable-kvm"]
    # 'host' n'existe qu'avec KVM ; sans KVM, 'max' est l'équivalent émulé.
    cmd += ["-cpu", cpu if kvm or cpu != "host" else "max"]
    if firmware == "uefi":
        cmd += [
            "-machine", "q35",
            "-drive", f"if=pflash,format=raw,readonly=on,file={OVMF_CODE}",
            "-drive", f"if=pflash,format=raw,file={vars_copy}",
        ]
    return cmd


def watch(cmd, marker, timeout, log_path):
    """Lance cmd, copie sa sortie dans log_path, renvoie True si marker apparaît avant timeout."""
    found = threading.Event()
    proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def reader():
        tail = b""
        with open(log_path, "wb") as log:
            while chunk := os.read(proc.stdout.fileno(), 4096):
                log.write(chunk)
                log.flush()
                # Le marqueur peut être coupé entre deux blocs.
                tail = (tail + chunk)[-(len(marker) + 4096):]
                if marker in tail:
                    found.set()

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()
    found.wait(timeout)
    proc.kill()
    proc.wait()
    thread.join(5)
    proc.stdout.close()
    return found.is_set()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("iso", type=Path)
    parser.add_argument("--firmware", choices=["bios", "uefi"], required=True)
    parser.add_argument("--cpu", default="host", help="modèle de CPU QEMU (host, qemu64…)")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--log", type=Path, default=Path("boot.log"))
    args = parser.parse_args()

    if not args.iso.is_file():
        print(f"ISO introuvable : {args.iso}", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        vars_copy = Path(tmp) / "OVMF_VARS.fd"
        if args.firmware == "uefi":
            shutil.copy(OVMF_VARS, vars_copy)
        ok = watch(qemu_command(args.iso, args.firmware, vars_copy, args.cpu), MARKER, args.timeout, args.log)
    print(f"démarrage {args.firmware}/{args.cpu} : {'OK' if ok else 'ÉCHEC'} (journal : {args.log})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
