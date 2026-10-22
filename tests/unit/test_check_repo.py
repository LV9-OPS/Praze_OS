# SPDX-License-Identifier: GPL-3.0-or-later
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import check_repo  # noqa: E402


class CheckRepoTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        for name in check_repo.REQUIRED_FILES:
            (self.root / name).write_bytes(b"ok\n")
        shutil.copy(REPO / "LICENSE", self.root / "LICENSE")

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_real_repo_is_clean(self):
        self.assertEqual(check_repo.check(REPO), [])

    def test_minimal_valid_tree(self):
        self.assertEqual(check_repo.check(self.root), [])

    def test_missing_required_file(self):
        (self.root / "SECURITY.md").unlink()
        self.assertIn("fichier requis absent : SECURITY.md", check_repo.check(self.root))

    def test_wrong_license(self):
        (self.root / "LICENSE").write_text("MIT License\n")
        self.assertIn("LICENSE n'est pas le texte GPL-3.0", check_repo.check(self.root))

    def test_crlf_detected(self):
        (self.root / "build.sh").write_bytes(b"#!/bin/sh\r\necho hi\r\n")
        self.assertIn("fins de ligne CRLF : build.sh", check_repo.check(self.root))

    def test_crlf_ignored_in_binary(self):
        (self.root / "logo.png").write_bytes(b"\x89PNG\r\n")
        self.assertEqual(check_repo.check(self.root), [])

    def test_private_key_detected(self):
        (self.root / "id").write_bytes(check_repo.PRIVATE_KEY_MARKER + b"\n")
        self.assertIn("clé privée détectée : id", check_repo.check(self.root))

    def test_skipped_dirs(self):
        (self.root / "target").mkdir()
        (self.root / "target" / "x.txt").write_bytes(b"a\r\n")
        self.assertEqual(check_repo.check(self.root), [])


if __name__ == "__main__":
    unittest.main()
