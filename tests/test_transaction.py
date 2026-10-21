from pathlib import Path
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from scripts.catalog import CatalogError
from scripts.transaction import commit_files, write_lock


class TransactionTests(unittest.TestCase):
    def test_success_updates_all_files_and_removes_journal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a, b = root / "a", root / "b"
            a.write_bytes(b"before")
            with write_lock(root):
                commit_files({a: "after", b: "new"}, root)
            self.assertEqual(a.read_bytes(), b"after")
            self.assertEqual(b.read_bytes(), b"new")
            self.assertFalse((root / ".cache/catalog-transaction").exists())

    def test_failure_rolls_back_existing_and_new_files_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a, b, c = [root / name for name in ("a", "new", "c")]
            original = b"original\r\n"
            a.write_bytes(original)
            c.write_bytes(b"last")
            real_replace = os.replace
            failed = False

            def fail_once(source, destination):
                nonlocal failed
                if Path(destination) == c and not failed:
                    failed = True
                    raise OSError("simulated full disk")
                return real_replace(source, destination)

            with write_lock(root), patch("scripts.transaction.os.replace", side_effect=fail_once):
                with self.assertRaises(OSError):
                    commit_files({a: "changed", b: "new", c: "changed"}, root)
            self.assertEqual(a.read_bytes(), original)
            self.assertFalse(b.exists())
            self.assertEqual(c.read_bytes(), b"last")

    def test_interrupted_write_is_recovered_before_next_reader(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "catalog.yaml"
            target.write_bytes(b"partial new data")
            journal = root / ".cache/catalog-transaction"
            journal.mkdir(parents=True)
            (journal / "old-0").write_bytes(b"original data")
            (journal / "manifest.json").write_text(json.dumps({
                "state": "prepared", "files": [{"path": "catalog.yaml", "existed": True}],
            }), encoding="utf-8")
            with write_lock(root):
                self.assertEqual(target.read_bytes(), b"original data")
            self.assertFalse(journal.exists())

    def test_committed_write_is_not_rolled_back_after_interruption(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "catalog.yaml"
            target.write_bytes(b"committed")
            journal = root / ".cache/catalog-transaction"
            journal.mkdir(parents=True)
            (journal / "old-0").write_bytes(b"original")
            (journal / "manifest.json").write_text(json.dumps({
                "state": "committed", "files": [{"path": "catalog.yaml", "existed": True}],
            }), encoding="utf-8")
            with write_lock(root):
                self.assertEqual(target.read_bytes(), b"committed")

    def test_writers_are_serialized(self):
        with tempfile.TemporaryDirectory() as directory:
            with write_lock(directory):
                with self.assertRaisesRegex(CatalogError, "Another catalog writer"):
                    with write_lock(directory):
                        self.fail("Concurrent writer was allowed")

    def test_failed_recovery_preserves_backup_for_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "a"
            target.write_bytes(b"original")
            real_replace = os.replace

            def unavailable(source, destination):
                if Path(destination) == target:
                    raise OSError("disk unavailable")
                return real_replace(source, destination)

            with write_lock(root), patch("scripts.transaction.os.replace", side_effect=unavailable):
                with self.assertRaisesRegex(CatalogError, "recovery is pending"):
                    commit_files({target: "new"}, root)
            self.assertTrue((root / ".cache/catalog-transaction/old-0").exists())
            with write_lock(root):
                pass
            self.assertEqual(target.read_bytes(), b"original")
            self.assertFalse((root / ".cache/catalog-transaction").exists())


if __name__ == "__main__":
    unittest.main()
