"""Offline tests for schema failures, refresh transactions, and generated documentation."""

from collections import Counter
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from scripts.catalog import (
    ROOT, CatalogError, load_catalog, save_catalog, sort_skills, validate, valid_url,
)
from scripts.check_links import anchors, check_links
from scripts.render_catalog import format_stars, render_all, replace_block, table
from scripts.update_stars import GitHubError, fetch_repository, main as update_main, refresh

NOW = "2026-10-21T06:00:00Z"


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = load_catalog()

    def test_shipped_catalog_has_valid_schema(self):
        self.assertEqual(validate(self.data), [])

    def test_initial_candidates_and_requested_addition_are_present(self):
        expected = {"frontend-design", "ui-ux-pro-max", "frontend-ui-engineering", "impeccable",
                    "domain-modeling", "api-and-interface-design", "api-design-reviewer",
                    "database-designer", "cloud-sql-basics", "karpathy-guidelines"}
        # Future additions are welcome; these original requested entries stay accounted for.
        self.assertTrue(expected <= {s["id"] for s in self.data["skills"]})
        initial = [s for s in self.data["skills"] if s["id"] in expected]
        self.assertEqual(Counter(s["category"] for s in initial),
                         {"frontend": 4, "backend": 3, "database": 2, "engineering": 1})

    def test_duplicate_ids_rejected(self):
        self.data["skills"].append(deepcopy(self.data["skills"][0]))
        self.assertTrue(any("duplicate ID" in e for e in validate(self.data)))

    def test_bad_shapes_return_errors(self):
        for value in (None, [], "wrong", {}, {"repositories": [], "skills": 3}):
            with self.subTest(value=value):
                self.assertTrue(validate(value))
        for section, value in (("skills", [None]), ("repositories", {"x/y": None})):
            broken = deepcopy(self.data)
            broken[section] = value
            self.assertTrue(validate(broken))

    def test_every_required_field_is_validated_before_rendering(self):
        for target in ("repository", "skill", "verification", "install"):
            for field in self._required_object(self.data, target):
                with self.subTest(target=target, field=field):
                    broken = deepcopy(self.data)
                    del self._required_object(broken, target)[field]
                    self.assertTrue(validate(broken))

    @staticmethod
    def _required_object(data, target):
        if target == "repository":
            return next(iter(data["repositories"].values()))
        if target == "skill":
            return data["skills"][0]
        return data["skills"][0][target]

    def test_invalid_skill_fields_rejected(self):
        for field, value in (("id", "Invalid ID"), ("category", "unknown"),
                             ("repository", "missing/repo"), ("repository", []),
                             ("tags", []), ("description", ""), ("skill_path", "../SKILL.md"),
                             ("skill_url", "https://example.com/wrong"), ("source_commit", "main"),
                             ("skill_updated_at", "yesterday"), ("verification", None), ("install", [])):
            with self.subTest(field=field, value=value):
                broken = deepcopy(self.data)
                broken["skills"][0][field] = value
                self.assertTrue(validate(broken))

    def test_invalid_star_counts_rejected_including_booleans(self):
        repo = next(iter(self.data["repositories"]))
        for value in (-1, True, 1.2, "123"):
            with self.subTest(value=value):
                broken = deepcopy(self.data)
                broken["repositories"][repo]["stars"] = value
                self.assertTrue(validate(broken))

    def test_unknown_stars_require_unknown_timestamp(self):
        meta = next(iter(self.data["repositories"].values()))
        meta["stars"] = None
        self.assertTrue(any("both" in e for e in validate(self.data)))
        meta["stars_updated_at"] = None
        sort_skills(self.data)
        self.assertEqual(validate(self.data), [])

    def test_naive_timestamp_rejected(self):
        next(iter(self.data["repositories"].values()))["stars_updated_at"] = "2026-10-21T06:00:00"
        self.assertTrue(validate(self.data))

    def test_repository_urls_and_license_evidence_checked(self):
        for field, value in (("url", "https://example.com"), ("license", None),
                             ("license", {"spdx": "MIT", "url": "http://example.com"})):
            broken = deepcopy(self.data)
            next(iter(broken["repositories"].values()))[field] = value
            self.assertTrue(validate(broken))

    def test_verification_flags_require_real_booleans(self):
        self.data["skills"][0]["verification"]["installation_tested"] = "false"
        self.assertTrue(validate(self.data))

    def test_verification_claims_need_evidence(self):
        for flag in ("installation_tested", "effectiveness"):
            with self.subTest(flag=flag):
                broken = deepcopy(self.data)
                broken["skills"][0]["verification"][flag] = True
                self.assertTrue(validate(broken))

    def test_unreviewed_install_command_rejected(self):
        self.data["skills"][0]["verification"]["installation"] = False
        self.assertTrue(validate(self.data))

    def test_sorting_puts_unknown_last_and_breaks_ties_by_id(self):
        repositories = {
            "a/a": {"stars": None}, "b/b": {"stars": 0},
            "c/c": {"stars": 20}, "d/d": {"stars": 20},
        }
        data = {"repositories": repositories, "skills": [
            {"id": "z", "category": "frontend", "repository": "c/c"},
            {"id": "u", "category": "frontend", "repository": "a/a"},
            {"id": "a", "category": "frontend", "repository": "d/d"},
            {"id": "b", "category": "frontend", "repository": "b/b"},
            {"id": "first", "category": "backend", "repository": "c/c"},
        ]}
        sort_skills(data)
        self.assertEqual([s["id"] for s in data["skills"]], ["a", "z", "b", "u", "first"])

    def test_unsorted_catalog_rejected(self):
        self.data["skills"].reverse()
        self.assertTrue(any("sorted" in e for e in validate(self.data)))

    def test_yaml_duplicate_keys_and_unsafe_tags_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.yaml"
            for content in ("version: 1\nversion: 2\n", "!!python/object/apply:os.system [echo bad]"):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(CatalogError):
                    load_catalog(path)

    def test_yaml_round_trip_preserves_timestamps_and_unicode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skills.yaml"
            save_catalog(self.data, path)
            self.assertEqual(load_catalog(path), self.data)
            self.assertEqual(list(Path(directory).glob("*.tmp")), [])

    def test_https_url_validation(self):
        for url in ("http://example.com", "https://", "https://[", "https://user:secret@example.com", "https://example.com/a b", None):
            self.assertFalse(valid_url(url))
        self.assertTrue(valid_url("https://github.com/owner/repo/blob/main/SKILL.md"))


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.data = load_catalog()

    def test_each_repository_fetched_once_and_shared_by_entries(self):
        fetcher = Mock(return_value=42)
        updated = refresh(self.data, fetcher, NOW)
        expected = {s["repository"] for s in self.data["skills"]}
        self.assertEqual(fetcher.call_count, len(expected))
        self.assertEqual({c.args[0] for c in fetcher.call_args_list}, expected)
        self.assertTrue(all(m["stars"] == 42 and m["stars_updated_at"] == NOW for m in updated["repositories"].values()))
        self.assertEqual(validate(updated), [])

    def test_failed_refresh_does_not_mutate_input(self):
        before = deepcopy(self.data)
        fetcher = Mock(side_effect=[42, GitHubError("rate limited")])
        with self.assertRaises(GitHubError):
            refresh(self.data, fetcher, NOW)
        self.assertEqual(self.data, before)

    def test_star_updates_do_not_renew_content_reviews(self):
        updated = refresh(self.data, lambda repo: 42, NOW)
        before = {s["id"]: s for s in self.data["skills"]}
        for skill in updated["skills"]:
            self.assertEqual(skill, before[skill["id"]])

    def test_invalid_fetcher_result_rejected(self):
        for value in (None, True, -1):
            with self.assertRaises(GitHubError):
                refresh(self.data, lambda repo: value, NOW)

    def test_api_authentication_and_timeout(self):
        opener = Mock(return_value=io.BytesIO(b'{"stargazers_count": 123}'))
        self.assertEqual(fetch_repository("a/b", token="unit-test-value", opener=opener), 123)
        request = opener.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.github.com/repos/a/b")
        self.assertEqual(request.get_header("Authorization"), "Bearer unit-test-value")
        self.assertEqual(opener.call_args.kwargs["timeout"], 20)

    def test_api_without_token_omits_authentication(self):
        opener = Mock(return_value=io.BytesIO(b'{"stargazers_count": 0}'))
        self.assertEqual(fetch_repository("a/b", opener=opener), 0)
        self.assertIsNone(opener.call_args.args[0].get_header("Authorization"))

    def test_rate_limits_and_missing_repository_are_actionable(self):
        for status in (403, 429, 404, 401):
            with self.subTest(status=status):
                error = HTTPError("https://api.github.com/repos/a/b", status, "error", {"X-RateLimit-Reset": "12345"}, None)
                opener = Mock(side_effect=error)
                with self.assertRaises(GitHubError) as result:
                    fetch_repository("a/b", token="unit-test-value", opener=opener)
                self.assertIn(str(status), str(result.exception))
                self.assertNotIn("unit-test-value", str(result.exception))
                self.assertEqual(opener.call_count, 1)

    def test_transient_server_error_retries_then_succeeds(self):
        error = HTTPError("url", 503, "error", {}, None)
        opener = Mock(side_effect=[error, io.BytesIO(b'{"stargazers_count": 5}')])
        sleeper = Mock()
        self.assertEqual(fetch_repository("a/b", opener=opener, sleeper=sleeper), 5)
        sleeper.assert_called_once_with(1)

    def test_network_failure_has_bounded_retries(self):
        opener = Mock(side_effect=URLError("connection failed"))
        sleeper = Mock()
        with self.assertRaisesRegex(GitHubError, "3 attempts"):
            fetch_repository("a/b", opener=opener, sleeper=sleeper)
        self.assertEqual(opener.call_count, 3)
        self.assertEqual([c.args[0] for c in sleeper.call_args_list], [1, 2])

    def test_bad_json_and_invalid_api_counts_rejected(self):
        for raw in (b'bad json', b'[]', b'{}', b'{"stargazers_count": true}', b'{"stargazers_count": -1}'):
            with self.subTest(raw=raw), self.assertRaises(GitHubError):
                fetch_repository("a/b", opener=Mock(return_value=io.BytesIO(raw)))

    def test_dry_run_changes_no_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog" / "skills.yaml"
            save_catalog(self.data, path)
            before = path.read_bytes()
            with patch("scripts.update_stars.fetch_repository", return_value=7), \
                 patch("scripts.update_stars.render_all", return_value={}), \
                 patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(update_main(["--catalog", str(path), "--dry-run"]), 0)
            self.assertEqual(path.read_bytes(), before)

    def test_failed_cli_leaves_catalog_and_docs_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog" / "skills.yaml"
            doc = Path(directory) / "README.md"
            save_catalog(self.data, path)
            doc.write_text("original", encoding="utf-8")
            before = path.read_bytes()
            with patch("scripts.update_stars.fetch_repository", side_effect=GitHubError("failure")), \
                 patch("sys.stderr", new_callable=io.StringIO):
                self.assertEqual(update_main(["--catalog", str(path)]), 1)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(doc.read_text(encoding="utf-8"), "original")

    def test_cli_refresh_saves_sorted_yaml_and_rendered_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog" / "skills.yaml"
            doc = Path(directory) / "README.md"
            save_catalog(self.data, path)
            with patch("scripts.update_stars.fetch_repository", return_value=19), \
                 patch("scripts.update_stars.render_all", return_value={doc: "updated\n"}), \
                 patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(update_main(["--catalog", str(path)]), 0)
            updated = load_catalog(path)
            self.assertEqual(validate(updated), [])
            self.assertTrue(all(m["stars"] == 19 for m in updated["repositories"].values()))
            self.assertEqual(doc.read_text(encoding="utf-8"), "updated\n")

    def test_gh_token_takes_precedence_over_github_token(self):
        with patch.dict("os.environ", {"GH_TOKEN": "first-test-value", "GITHUB_TOKEN": "second-test-value"}), \
             patch("scripts.update_stars.fetch_repository", return_value=7) as fetcher, \
             patch("scripts.update_stars.render_all", return_value={}), \
             patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(update_main(["--dry-run"]), 0)
            self.assertTrue(all(c.args[1] == "first-test-value" for c in fetcher.call_args_list))


class DocumentationTests(unittest.TestCase):
    def test_generated_files_match_catalog(self):
        for path, output in render_all(load_catalog()).items():
            with self.subTest(path=path.name):
                self.assertEqual(path.read_text(encoding="utf-8"), output)

    def test_generator_is_idempotent_and_preserves_editorial_copy(self):
        original = "Editorial\n<!-- BEGIN x -->\nold\n<!-- END x -->\nFooter\n"
        rendered = replace_block(original, "x", "new")
        self.assertEqual(rendered, replace_block(rendered, "x", "new"))
        self.assertTrue(rendered.startswith("Editorial\n"))
        self.assertTrue(rendered.endswith("Footer\n"))

    def test_missing_or_duplicate_markers_fail(self):
        for text in ("", "<!-- BEGIN x --><!-- BEGIN x --><!-- END x -->", "<!-- END x --><!-- BEGIN x -->"):
            with self.assertRaises(CatalogError):
                replace_block(text, "x", "value")

    def test_star_format_and_unknown_display(self):
        self.assertEqual([format_stars(x) for x in (None, 0, 999, 1000, 12543)],
                         ["N/A", "0", "999", "1.0k", "12.5k"])
        data = load_catalog()
        for meta in data["repositories"].values():
            meta["stars"] = None
            meta["stars_updated_at"] = None
        self.assertIn("N/A", table(data, "frontend"))

    def test_markdown_local_links_and_anchors(self):
        errors, count = check_links()
        self.assertGreater(count, 50)
        self.assertEqual(errors, [])

    def test_broken_links_are_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Title\n[a](absent.md)\n[b](#absent)\n[c](../outside.md)\n", encoding="utf-8")
            errors, count = check_links(root)
            self.assertEqual(count, 3)
            self.assertEqual(len(errors), 3)

    def test_code_examples_do_not_create_links_or_anchors(self):
        self.assertEqual(anchors('# Visible\n```md\n# Hidden\n```\n<a id="explicit"></a>\n'), {"visible", "explicit"})


if __name__ == "__main__":
    unittest.main()
