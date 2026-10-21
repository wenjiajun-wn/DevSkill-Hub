"""Run fixed-version installers in disposable project directories, never globally.

Install tools first with npm --prefix .cache/tools, as documented in the report.
This script does not start model sessions, run hooks, or provision cloud resources.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

try:
    from .catalog import ROOT, atomic_write
except ImportError:
    from catalog import ROOT, atomic_write


def plans(tools):
    node = shutil.which("node")
    if not node:
        raise RuntimeError("Node.js is required for installation smoke tests")
    modules = Path(tools).resolve() / "node_modules"
    claude = [node, str(modules / "@anthropic-ai/claude-code/cli-wrapper.cjs")]
    skills = [node, str(modules / "skills/bin/cli.mjs")]
    ui = [node, str(modules / "ui-ux-pro-max-cli/dist/index.js")]
    impeccable = [node, str(modules / "impeccable/cli/bin/cli.js")]

    def plugin(repo, bundle):
        add = claude + ["plugin", "marketplace", "add", repo, "--scope", "project", "--json"]
        if repo == "alirezarezvani/claude-skills":
            add += ["--sparse", ".claude-plugin", "engineering"]
        if repo == "pbakaus/impeccable":
            add += ["--sparse", ".claude-plugin", "plugin"]
        return [add, claude + ["plugin", "install", bundle, "--scope", "project", "--json"]]

    return [
        ("anthropic", ["frontend-design"], plugin("anthropics/skills", "example-skills@anthropic-agent-skills")),
        ("ui-pro-max", ["ui-ux-pro-max"], [ui + ["init", "--ai", "codex"]]),
        ("addy", ["frontend-ui-engineering", "api-and-interface-design"], plugin("addyosmani/agent-skills", "agent-skills@addy-agent-skills")),
        ("impeccable", ["impeccable"], plugin("pbakaus/impeccable", "impeccable@impeccable")),
        ("matt", ["domain-modeling"], [skills + ["add", "mattpocock/skills", "--skill", "domain-modeling", "setup-matt-pocock-skills", "--agent", "codex", "--copy", "--yes", "--full-depth", "--json"]]),
        ("alireza", ["api-design-reviewer", "database-designer"], plugin("alirezarezvani/claude-skills", "engineering-advanced-skills@claude-code-skills")),
        ("google", ["cloud-sql-basics"], [skills + ["add", "google/skills", "--skill", "cloud-sql-basics", "--agent", "codex", "--copy", "--yes", "--full-depth", "--json"]]),
        ("karpathy", ["karpathy-guidelines"], plugin("multica-ai/andrej-karpathy-skills", "andrej-karpathy-skills@karpathy-skills")),
    ]


def run_plan(plan, workspace):
    name, ids, commands = plan
    project = workspace / name
    project.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["CLAUDE_CONFIG_DIR"] = str(project / "claude-config")
    env["IMPECCABLE_HOME"] = str(project / "impeccable-runtime")
    env["CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS"] = "300000"
    env["CI"] = "1"
    records = []
    for index, command in enumerate(commands):
        try:
            process = subprocess.run(command, cwd=project, env=env, capture_output=True,
                                     text=True, encoding="utf-8", errors="replace", timeout=420)
            output = process.stdout + "\n" + process.stderr
            output = re.sub(r"\x1b\[[0-9;]*m", "", output)
            atomic_write(project / f"command-{index}.log", output)
            # Public report contains no raw tool output, credentials, or local paths.
            records.append({"arguments": command[2:], "exit_code": process.returncode})
            if process.returncode != 0:
                break
        except subprocess.TimeoutExpired:
            records.append({"arguments": command[2:], "exit_code": "timeout"})
            break
    installed = {}
    for skill_id in ids:
        matches = list(project.rglob(f"{skill_id}/SKILL.md"))
        installed[skill_id] = [path.relative_to(project).as_posix() for path in matches]
    passed = bool(records) and len(records) == len(commands) and all(r["exit_code"] == 0 for r in records) and all(installed.values())
    result = {"plan": name, "skills": ids, "passed": passed, "commands": records, "installed_skill_files": installed}
    print(f"{name}: {'PASS' if passed else 'FAIL'}", flush=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools", type=Path, default=ROOT / ".cache/tools")
    parser.add_argument("--workspace", type=Path, default=ROOT / ".cache/installation-smoke")
    parser.add_argument("--only", help="Comma-separated plan names to rerun")
    args = parser.parse_args(argv)
    chosen = [p for p in plans(args.tools) if not args.only or p[0] in args.only.split(",")]
    if not chosen:
        raise RuntimeError("No smoke installation plans selected")
    workspace = args.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda plan: run_plan(plan, workspace), chosen))
    path = workspace / "results.json"
    if args.only and path.exists():
        old = json.loads(path.read_text(encoding="utf-8"))["results"]
        names = {r["plan"] for r in results}
        results = [r for r in old if r["plan"] not in names] + results
    report = {"observed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "os": platform.system(), "python": platform.python_version(), "results": results}
    atomic_write(path, json.dumps(report, indent=2))
    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
