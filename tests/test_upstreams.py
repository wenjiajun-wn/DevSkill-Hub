from copy import deepcopy
import io
import unittest
from unittest.mock import Mock

from scripts.catalog import CatalogError
from scripts.check_upstreams import fetch_tree, inspect_catalog, report


class UpstreamTests(unittest.TestCase):
    def setUp(self):
        self.data = {"repositories": {"owner/repo": {"url": "https://github.com/owner/repo",
            "default_branch": "main", "monitoring": {"reviewed_at": "2026-10-21T00:00:00Z",
            "files": {"skills/example": "a" * 40, "README.md": "b" * 40, "LICENSE": None}}}}}

    def test_unchanged_tree_produces_stable_report(self):
        fetcher = Mock(return_value={"skills/example": "a" * 40, "README.md": "b" * 40})
        self.assertEqual(inspect_catalog(self.data, fetcher), [])
        self.assertEqual(report(self.data, []), report(self.data, []))
        fetcher.assert_called_once_with("owner/repo", "main")

    def test_changed_skill_removed_readme_and_new_license_are_detected(self):
        before = deepcopy(self.data)
        findings = inspect_catalog(self.data, lambda repo, branch: {"skills/example": "c" * 40, "LICENSE": "d" * 40})
        self.assertEqual([f["status"] for f in findings], ["changed", "removed", "added"])
        self.assertEqual(self.data, before)

    def test_missing_baseline_fails_without_silently_establishing_one(self):
        del self.data["repositories"]["owner/repo"]["monitoring"]
        with self.assertRaisesRegex(CatalogError, "missing reviewed"):
            inspect_catalog(self.data, Mock())

    def test_truncated_api_tree_is_not_treated_as_no_changes(self):
        opener = Mock(return_value=io.BytesIO(b'{"tree": [], "truncated": true}'))
        with self.assertRaisesRegex(CatalogError, "incomplete"):
            fetch_tree("owner/repo", "main", opener=opener)

    def test_branch_is_url_encoded(self):
        opener = Mock(return_value=io.BytesIO(b'{"tree": [], "truncated": false}'))
        self.assertEqual(fetch_tree("owner/repo", "release/v1", opener=opener), {})
        self.assertIn("release%2Fv1", opener.call_args.args[0].full_url)


if __name__ == "__main__":
    unittest.main()
