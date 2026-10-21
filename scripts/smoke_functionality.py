"""Exercise installed upstream tools against original, bounded offline fixtures."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

try:
    from .catalog import ROOT, atomic_write
except ImportError:
    from catalog import ROOT, atomic_write


def find_skill(cache, skill_id):
    matches = list(cache.rglob(f"{skill_id}/SKILL.md"))
    installed = [path for path in matches if "/plugins/cache/" in path.as_posix() or "/.agents/skills/" in path.as_posix()]
    if not installed:
        raise RuntimeError(f"Install {skill_id} first with scripts/smoke_install.py")
    return installed[0].parent


def execute(command, cwd, expected_codes=(0,)):
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["IMPECCABLE_HOME"] = str(ROOT / ".cache/functional-smoke/impeccable")
    process = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=60)
    if process.returncode not in expected_codes:
        raise RuntimeError(f"Tool failed with exit {process.returncode}; see .cache/functional-smoke logs")
    return process, json.loads(process.stdout)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache")
    parser.add_argument("--allow-known-limitations", action="store_true", help="Accept the recorded upstream SQL-parser limitation if the JSON alternative passes")
    args = parser.parse_args(argv)
    work = ROOT / ".cache/functional-smoke"
    work.mkdir(parents=True, exist_ok=True)
    fixture = ROOT / "docs/evaluations/fixtures"
    with sqlite3.connect(":memory:") as database_engine:
        database_engine.executescript((fixture / "schema.sql").read_text(encoding="utf-8"))
        engine_foreign_keys = len(database_engine.execute("PRAGMA foreign_key_list(skill_entries)").fetchall())
        assert engine_foreign_keys == 1, "Original SQL fixture must contain one engine-verified foreign key"
    spec = {"openapi": "3.0.3", "info": {"title": "Registry fixture", "version": "1.0.0"},
            "paths": {"/getUsers": {"get": {"responses": {"200": {"description": "OK"}}}}}}
    old, new = work / "old.json", work / "new.json"
    atomic_write(old, json.dumps(spec))
    atomic_write(new, json.dumps({**spec, "paths": {}}))
    ui = find_skill(args.cache, "ui-ux-pro-max")
    api = find_skill(args.cache, "api-design-reviewer")
    database = find_skill(args.cache, "database-designer")
    commands = {
        "ui-search": [sys.executable, str(ui / "scripts/search.py"), "keyboard focus visible", "--domain", "ux", "--json"],
        "api-lint": [sys.executable, str(api / "scripts/api_linter.py"), str(old), "--format", "json"],
        "api-breaking-change": [sys.executable, str(api / "scripts/breaking_change_detector.py"), str(old), str(new), "--format", "json", "--exit-on-breaking"],
        "database-schema": [sys.executable, str(database / "schema_analyzer.py"), "--input", str(fixture / "schema.sql"), "--output-format", "json", "--generate-erd"],
        "database-json": [sys.executable, str(database / "schema_analyzer.py"), "--input", str(fixture / "schema.json"), "--output-format", "json", "--generate-erd"],
        "ui-detector": [shutil.which("node"), str(args.cache / "tools/node_modules/impeccable/cli/bin/cli.js"), "detect", str(fixture / "problematic-ui.html"), "--json", "--no-config"],
    }
    results = {}
    for name, command in commands.items():
        process, output = execute(command, ROOT, expected_codes=(0, 1) if name == "api-breaking-change" else (0, 2) if name == "ui-detector" else (0,))
        atomic_write(work / f"{name}.json", json.dumps(output, ensure_ascii=False, indent=2))
        results[name] = {"exit_code": process.returncode, "output": output}
        print(f"{name}: tool executed; exit {process.returncode}", flush=True)
    results["observed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    checks = {
        "ui-search": results["ui-search"]["output"].get("count", 0) > 0 and any("focus" in row.get("Issue", "").lower() for row in results["ui-search"]["output"].get("results", [])),
        "api-lint": any(issue.get("category") == "naming" for issue in results["api-lint"]["output"].get("issues", [])),
        "api-breaking-change": results["api-breaking-change"]["exit_code"] == 1 and results["api-breaking-change"]["output"].get("hasBreakingChanges") is True,
        "database-schema": results["database-schema"]["output"].get("schema_overview", {}).get("total_foreign_keys") == 1,
        "database-json": results["database-json"]["output"].get("schema_overview", {}).get("total_foreign_keys") == 1,
        "ui-detector": results["ui-detector"]["exit_code"] == 2 and any(f.get("antipattern") == "gradient-text" for f in results["ui-detector"]["output"]),
    }
    results["acceptance"] = checks
    atomic_write(work / "results.json", json.dumps(results, ensure_ascii=False, indent=2))
    # Publish concise original observations, not third-party tool source or full diagnostics.
    summary = {"observed_at": results["observed_at"], "acceptance": checks,
        "observations": {
            "ui_search_results": results["ui-search"]["output"]["count"],
            "api_lint_issues": results["api-lint"]["output"]["summary"]["total_issues"],
            "breaking_changes": results["api-breaking-change"]["output"]["summary"]["breaking_changes"],
            "sql_tables": results["database-schema"]["output"]["schema_overview"]["total_tables"],
            "sql_foreign_keys": results["database-schema"]["output"]["schema_overview"]["total_foreign_keys"],
            "sqlite_verified_foreign_keys": engine_foreign_keys,
            "json_foreign_keys": results["database-json"]["output"]["schema_overview"]["total_foreign_keys"],
            "ui_findings": len(results["ui-detector"]["output"]),
        }, "scope": "Offline tool smoke checks; no model comparison, rendered browser review, or cloud provisioning."}
    atomic_write(ROOT / "docs/evaluations/functionality.json", json.dumps(summary, indent=2) + "\n")
    failures = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"Acceptance {name}: {'PASS' if passed else 'FAIL'}")
    accepted = args.allow_known_limitations and failures == ["database-schema"] and checks["database-json"]
    return 0 if not failures or accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
