"""Publish sanitized installation evidence from the disposable smoke workspaces."""

import hashlib
import json
from pathlib import Path

import yaml

try:
    from .catalog import ROOT, atomic_write
except ImportError:
    from catalog import ROOT, atomic_write

RESOURCES = {
    "frontend-design": ["LICENSE.txt"],
    "ui-ux-pro-max": ["scripts/search.py", "data"],
    "frontend-ui-engineering": ["../../references/accessibility-checklist.md"],
    "api-and-interface-design": ["../../references"],
    "domain-modeling": ["GLOSSARY-FORMAT.md", "ADR-FORMAT.md"],
    "api-design-reviewer": ["scripts/api_linter.py", "scripts/breaking_change_detector.py"],
    "database-designer": ["schema_analyzer.py", "index_optimizer.py"],
    "cloud-sql-basics": ["references/iac-usage.md", "references/iam-security.md"],
    "impeccable": ["scripts/impeccable.cmd", "reference"],
    "karpathy-guidelines": [],
}


def main():
    records = {}
    attempts = []
    for workspace in ("installation-smoke", "installation-smoke-retry", "installation-smoke-plugin"):
        root = ROOT / ".cache" / workspace
        result_path = root / "results.json"
        if not result_path.exists():
            continue
        report = json.loads(result_path.read_text(encoding="utf-8"))
        for result in report["results"]:
            attempts.append({"plan": result["plan"], "passed": result["passed"], "observed_at": report["observed_at"]})
            if not result["passed"]:
                continue
            for skill_id in result["skills"]:
                paths = result["installed_skill_files"][skill_id]
                selected = next((p for p in paths if "/plugins/cache/" in p), paths[0])
                skill = root / result["plan"] / selected
                content = skill.read_text(encoding="utf-8")
                metadata = yaml.safe_load(content.split("---", 2)[1])
                resources = {name: (skill.parent / name).exists() for name in RESOURCES[skill_id]}
                passed = metadata.get("name") == skill_id and bool(metadata.get("description")) and all(resources.values())
                records[skill_id] = {"passed": passed, "observed_at": report["observed_at"],
                    "platform": report["os"], "scope": "isolated project", "skill_sha256": hashlib.sha256(skill.read_bytes()).hexdigest(),
                    "installed_path": selected, "supporting_resources": resources,
                    "commands": result["commands"]}
    tools = ROOT / ".cache/tools/node_modules"
    versions = {name: json.loads((tools / name / "package.json").read_text(encoding="utf-8"))["version"]
                for name in ("@anthropic-ai/claude-code", "skills", "ui-ux-pro-max-cli", "impeccable")}
    output = {"tools": versions, "attempts": attempts, "skills": records,
              "scope": "Installer execution, installed SKILL.md identity, and supporting-file presence only; no model activation or comparative quality claim."}
    atomic_write(ROOT / "docs/evaluations/installations.json", json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Installation smoke tests / 安装冒烟测试", "This report records actual installer execution in disposable Windows project directories. No user-level skills were installed, no model sessions were started, and hooks were not executed. Published evidence contains tool versions, exit codes, file identity hashes, and supporting-file checks; temporary source files and logs are not redistributed.",
             "在 Windows 临时项目目录实际安装，检查退出状态、Skill 身份和配套文件。没有改动用户级 Skills，没有启动模型会话或执行 Hook。此结果不等于验证所有平台的自动发现与实际效果。",
             "## Reproduce / 复现\n\nRequires Python 3.11+, Node.js 22.20+, Git, and public network access.\n\n```bash\nnpm install --prefix .cache/tools --no-audit --no-fund --ignore-scripts @anthropic-ai/claude-code@2.1.306 skills@1.7.4 ui-ux-pro-max-cli@2.15.0 impeccable@4.7.0\npython scripts/smoke_install.py\npython scripts/publish_smoke_results.py\n```",
             "The test invokes Anthropic's documented fallback launcher because dependency lifecycle scripts are disabled. Marketplace and plugin installation use `--scope project` with an isolated `CLAUDE_CONFIG_DIR`. Sparse checkout retains the selected plugin domain. The same source's two catalog skills share one installed bundle.",
             "## Results / 结果\n\n| Skill | Install + identity + resources | Observed (UTC) |\n| --- | --- | --- |"]
    for skill_id, record in sorted(records.items()):
        lines.append(f"| [{skill_id}](#{skill_id}) | {'PASS' if record['passed'] else 'FAIL'} | {record['observed_at']} |")
    for skill_id, record in sorted(records.items()):
        lines.append(f'\n<a id="{skill_id}"></a>\n\n## {skill_id}\n\nProject installation: **{"PASS" if record["passed"] else "FAIL"}**. `SKILL.md` SHA-256: `{record["skill_sha256"]}`.\n\nSupporting files checked: ' + (", ".join(f"`{p}`" for p in record["supporting_resources"]) or "no additional files required") + ".")
    lines += ["\n## Findings / 发现", "- Karpathy's canonical `multica-ai/andrej-karpathy-skills` marketplace installed successfully; the catalog can use that tested address instead of the legacy owner.\n- Impeccable's release-bundle installer timed out twice in this network. The documented Claude Code plugin method installed successfully instead. This is a tested alternative, not a claim the original release endpoint works everywhere.\n- The full advanced-engineering clone timed out. The official CLI's sparse-checkout option succeeded and retained both selected skills and their tools.\n- Full Addy plugin installation preserved repository-level references that individual-skill copies can omit.\n- Google's installer warned about invalid frontmatter in an unrelated Ads skill; the selected Cloud SQL skill installed successfully.",
              "\n[Machine-readable evidence](installations.json) · [Functional evaluations](functional-smoke.md). Installation evidence is platform- and version-specific. It does not establish improvement over a baseline, agent auto-activation, cloud integration, or comprehensive security."]
    atomic_write(ROOT / "docs/evaluations/installation-smoke.md", "\n\n".join(lines[:5]) + "\n\n" + "\n".join(lines[5:]) + "\n")
    failed = [name for name in RESOURCES if not records.get(name, {}).get("passed")]
    print(f"Published installation evidence: {len(records) - len(failed)} passed; missing/failed: {', '.join(failed) or 'none'}")
    return bool(failed)


if __name__ == "__main__":
    raise SystemExit(main())
