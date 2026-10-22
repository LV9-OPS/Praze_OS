# SPDX-License-Identifier: GPL-3.0-or-later
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tests" / "vm"))

import boot_iso  # noqa: E402


def fake_vm(script):
    return [sys.executable, "-c", script]


class WatchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.log = self.tmp / "boot.log"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_marker_without_newline(self):
        cmd = fake_vm("import sys,time; sys.stdout.write('archiso login: '); sys.stdout.flush(); time.sleep(30)")
        self.assertTrue(boot_iso.watch(cmd, b"login:", 10, self.log))
        self.assertIn(b"archiso login:", self.log.read_bytes())

    def test_timeout_without_marker(self):
        cmd = fake_vm("import time; print('Booting...', flush=True); time.sleep(30)")
        self.assertFalse(boot_iso.watch(cmd, b"login:", 1, self.log))
        self.assertIn(b"Booting...", self.log.read_bytes())

    def test_process_exits_early(self):
        cmd = fake_vm("print('kernel panic')")
        self.assertFalse(boot_iso.watch(cmd, b"login:", 2, self.log))


class CommandTest(unittest.TestCase):
    def test_uefi_uses_ovmf(self):
        cmd = boot_iso.qemu_command("lv8.iso", "uefi", "/tmp/vars.fd")
        self.assertIn(f"if=pflash,format=raw,readonly=on,file={boot_iso.OVMF_CODE}", cmd)
        self.assertIn("if=pflash,format=raw,file=/tmp/vars.fd", cmd)

    def test_bios_has_no_pflash(self):
        cmd = boot_iso.qemu_command("lv8.iso", "bios", "/tmp/vars.fd")
        self.assertFalse(any("pflash" in arg for arg in cmd))
        self.assertIn("lv8.iso", cmd)


if __name__ == "__main__":
    unittest.main()
