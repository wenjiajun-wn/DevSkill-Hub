# Installation smoke tests / 安装冒烟测试

This report records actual installer execution in disposable Windows project directories. No user-level skills were installed, no model sessions were started, and hooks were not executed. Published evidence contains tool versions, exit codes, file identity hashes, and supporting-file checks; temporary source files and logs are not redistributed.

在 Windows 临时项目目录实际安装，检查退出状态、Skill 身份和配套文件。没有改动用户级 Skills，没有启动模型会话或执行 Hook。此结果不等于验证所有平台的自动发现与实际效果。

## Reproduce / 复现

Requires Python 3.11+, Node.js 22.20+, Git, and public network access.

```bash
npm install --prefix .cache/tools --no-audit --no-fund --ignore-scripts @anthropic-ai/claude-code@2.1.306 skills@1.7.4 ui-ux-pro-max-cli@2.15.0 impeccable@4.7.0
python scripts/smoke_install.py
python scripts/publish_smoke_results.py
```

The test invokes Anthropic's documented fallback launcher because dependency lifecycle scripts are disabled. Marketplace and plugin installation use `--scope project` with an isolated `CLAUDE_CONFIG_DIR`. Sparse checkout retains the selected plugin domain. The same source's two catalog skills share one installed bundle.

## Results / 结果

| Skill | Install + identity + resources | Observed (UTC) |
| --- | --- | --- |
| [api-and-interface-design](#api-and-interface-design) | PASS | 2026-10-21T06:49:24+00:00 |
| [api-design-reviewer](#api-design-reviewer) | PASS | 2026-10-21T06:57:46+00:00 |
| [cloud-sql-basics](#cloud-sql-basics) | PASS | 2026-10-21T06:49:24+00:00 |
| [database-designer](#database-designer) | PASS | 2026-10-21T06:57:46+00:00 |
| [domain-modeling](#domain-modeling) | PASS | 2026-10-21T06:49:24+00:00 |
| [frontend-design](#frontend-design) | PASS | 2026-10-21T06:49:24+00:00 |
| [frontend-ui-engineering](#frontend-ui-engineering) | PASS | 2026-10-21T06:49:24+00:00 |
| [impeccable](#impeccable) | PASS | 2026-10-21T06:57:46+00:00 |
| [karpathy-guidelines](#karpathy-guidelines) | PASS | 2026-10-21T06:49:24+00:00 |
| [ui-ux-pro-max](#ui-ux-pro-max) | PASS | 2026-10-21T06:49:24+00:00 |

<a id="api-and-interface-design"></a>

## api-and-interface-design

Project installation: **PASS**. `SKILL.md` SHA-256: `e83d34f52ff12dd8a7c5134cd7e8140ea4541ec65e204f8a1e4cd366e30c4192`.

Supporting files checked: `../../references`.

<a id="api-design-reviewer"></a>

## api-design-reviewer

Project installation: **PASS**. `SKILL.md` SHA-256: `984d644fd5d0ef8fcdb22673491f6097f389cba344665d15595c6420e977f66f`.

Supporting files checked: `scripts/api_linter.py`, `scripts/breaking_change_detector.py`.

<a id="cloud-sql-basics"></a>

## cloud-sql-basics

Project installation: **PASS**. `SKILL.md` SHA-256: `23ab14d93627070b659ed25b297c8530789706cda698d0ed6e4c900ac1427ccd`.

Supporting files checked: `references/iac-usage.md`, `references/iam-security.md`.

<a id="database-designer"></a>

## database-designer

Project installation: **PASS**. `SKILL.md` SHA-256: `2631b1cc6f005e5bc450227c3f91e77e3469bc55d9eaaec04c5fc85924127bd3`.

Supporting files checked: `schema_analyzer.py`, `index_optimizer.py`.

<a id="domain-modeling"></a>

## domain-modeling

Project installation: **PASS**. `SKILL.md` SHA-256: `b62d997256cc073e123d4303da8e9db00db0e28de9739660ca3e55ab76e09cdb`.

Supporting files checked: `GLOSSARY-FORMAT.md`, `ADR-FORMAT.md`.

<a id="frontend-design"></a>

## frontend-design

Project installation: **PASS**. `SKILL.md` SHA-256: `b8009ae690dfa69edc7f08bb8715f32db8817112cfa4388741dbaf876c237df8`.

Supporting files checked: `LICENSE.txt`.

<a id="frontend-ui-engineering"></a>

## frontend-ui-engineering

Project installation: **PASS**. `SKILL.md` SHA-256: `29a3e53d57c0a128831a20730ae874a8c4fda40c001fcdc15f8e9ad4b5f72f1b`.

Supporting files checked: `../../references/accessibility-checklist.md`.

<a id="impeccable"></a>

## impeccable

Project installation: **PASS**. `SKILL.md` SHA-256: `033806203a5e05efe3b67c9d72fa597c40263d6ac95959701336d593b1069ce1`.

Supporting files checked: `scripts/impeccable.cmd`, `reference`.

<a id="karpathy-guidelines"></a>

## karpathy-guidelines

Project installation: **PASS**. `SKILL.md` SHA-256: `e2553e9b66299fbca399804d6c44dfa44b2384b979ca5bf8b933b4916bb3141b`.

Supporting files checked: no additional files required.

<a id="ui-ux-pro-max"></a>

## ui-ux-pro-max

Project installation: **PASS**. `SKILL.md` SHA-256: `e5baf9400d4347e5ed3eb1f6b99cd0b9ba545b8b0e507aabb2b87397bbf73ea1`.

Supporting files checked: `scripts/search.py`, `data`.

## Findings / 发现
- Karpathy's canonical `multica-ai/andrej-karpathy-skills` marketplace installed successfully; the catalog can use that tested address instead of the legacy owner.
- Impeccable's release-bundle installer timed out twice in this network. The documented Claude Code plugin method installed successfully instead. This is a tested alternative, not a claim the original release endpoint works everywhere.
- The full advanced-engineering clone timed out. The official CLI's sparse-checkout option succeeded and retained both selected skills and their tools.
- Full Addy plugin installation preserved repository-level references that individual-skill copies can omit.
- Google's installer warned about invalid frontmatter in an unrelated Ads skill; the selected Cloud SQL skill installed successfully.

[Machine-readable evidence](installations.json) · [Functional evaluations](functional-smoke.md). Installation evidence is platform- and version-specific. It does not establish improvement over a baseline, agent auto-activation, cloud integration, or comprehensive security.
