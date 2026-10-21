# DevSkill Hub

**Discover, Install, and Master the Best Developer Agent Skills.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

English · [简体中文](README.zh-CN.md)

A curated collection of high-quality Agent Skills for frontend, backend, database, and modern software development. A focused directory for developers working with Codex, Claude Code, Cursor, and other coding agents.

<!-- BEGIN summary -->
**v0.1.0 · 10 skills · 8 source repositories**

Frontend Development 4 / Backend Development 3 / Database Development 2 / Engineering Practices 1
<!-- END summary -->

[Frontend](#frontend) · [Backend](#backend) · [Database](#database) · [Engineering](#engineering) · [Getting started](docs/getting-started.md) · [Contributing](CONTRIBUTING.md)

## Why a skills directory?

Agent Skills package task-specific instructions, references, and optional tools around a `SKILL.md` entry point. They give an agent reusable working practices, from accessible UI components to API review and data modeling.

Finding useful skills means checking scattered repositories, changing paths, installation details, and licensing. This registry keeps those facts together, with source links and explicit verification states. It indexes upstream work; it does not redistribute third-party skills.

## Quick start

1. Choose a task in the catalog below. Open its **Install** link for the verified upstream method and caveats.
2. Review the upstream files and follow the instructions for your agent. A published command does not mean we have executed it.
3. Try one skill on a small, reviewable change and inspect the result.

<!-- BEGIN quick-install -->
For example, upstream documents this installation entry point ([source](https://github.com/addyosmani/agent-skills#quick-start)):

```text
npx skills add addyosmani/agent-skills
```
<!-- END quick-install -->

This is a repository-level installer, not a promise to install only one skill. Read the [installation guide](docs/how-to-install.md), including the upstream warning about supplementary shared references in individual-skill installs. Claude Code plugin commands must be entered inside Claude Code; they are not shell commands.

## Read the verification labels

- **Metadata reviewed**: actual `SKILL.md`, category fit, source revision, license evidence, and upstream documentation inspected.
- **Install instructions reviewed**: command or workflow appears in upstream documentation; **installation executed** is tracked separately.
- **Effectiveness tested**: requires a recorded task and outcome. No entry currently claims this.

See [evaluation criteria](docs/evaluation-criteria.md) and the [verification record](docs/verification.md). Popularity is one navigation aid, not a quality benchmark.

<!-- BEGIN catalog -->
Stars observed (UTC): **2026-10-21T05:55:49Z**.

Stars belong to the source repository, not the individual skill. They measure popularity, not effectiveness. N/A means no verified data.

<a id="frontend"></a>

## Frontend Development

| Rank | Skill | Description | Repository Stars | Install |
| ---: | --- | --- | ---: | --- |
| 1 | [Frontend Design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Distinctive visual direction, typography, and intentional interface design. | [182.5k](https://github.com/anthropics/skills) | [Install](catalog/frontend.md#frontend-design) |
| 2 | [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/.claude/skills/ui-ux-pro-max/SKILL.md) | Searchable design guidance for palettes, typography, accessibility, and frontend stacks. | [138.1k](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | [Install](catalog/frontend.md#ui-ux-pro-max) |
| 3 | [Frontend UI Engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/frontend-ui-engineering/SKILL.md) | Component architecture, responsive layouts, state management, and accessible UI. | [109.1k](https://github.com/addyosmani/agent-skills) | [Install](catalog/frontend.md#frontend-ui-engineering) |
| 4 | [Impeccable](https://github.com/pbakaus/impeccable/blob/main/.agents/skills/impeccable/SKILL.md) | Audit, critique, polish, and animate interfaces with a focused design workflow. | [84.0k](https://github.com/pbakaus/impeccable) | [Install](catalog/frontend.md#impeccable) |

<a id="backend"></a>

## Backend Development

| Rank | Skill | Description | Repository Stars | Install |
| ---: | --- | --- | ---: | --- |
| 1 | [Domain Modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md) | Clarify domain terminology, challenge edge cases, and maintain glossaries and ADRs. | [298.9k](https://github.com/mattpocock/skills) | [Install](catalog/backend.md#domain-modeling) |
| 2 | [API and Interface Design](https://github.com/addyosmani/agent-skills/blob/main/skills/api-and-interface-design/SKILL.md) | Contract-first interfaces, compatibility, boundary validation, and error semantics. | [109.1k](https://github.com/addyosmani/agent-skills) | [Install](catalog/backend.md#api-and-interface-design) |
| 3 | [API Design Reviewer](https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skills/api-design-reviewer/SKILL.md) | Review REST conventions and OpenAPI contracts with linting and breaking-change checks. | [28.5k](https://github.com/alirezarezvani/claude-skills) | [Install](catalog/backend.md#api-design-reviewer) |

<a id="database"></a>

## Database Development

| Rank | Skill | Description | Repository Stars | Install |
| ---: | --- | --- | ---: | --- |
| 1 | [Database Designer](https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skills/database-designer/SKILL.md) | Schema modeling, index analysis, relationships, and migration planning. | [28.5k](https://github.com/alirezarezvani/claude-skills) | [Install](catalog/database.md#database-designer) |
| 2 | [Cloud SQL Basics](https://github.com/google/skills/blob/main/skills/cloud/cloud-sql-basics/SKILL.md) | Guide Cloud SQL instances, databases, backups, availability, and secure connectivity. | [21.5k](https://github.com/google/skills) | [Install](catalog/database.md#cloud-sql-basics) |

<a id="engineering"></a>

## Engineering Practices

| Rank | Skill | Description | Repository Stars | Install |
| ---: | --- | --- | ---: | --- |
| 1 | [Karpathy Guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md) | Reduce coding mistakes with explicit assumptions, simplicity, focused edits, and verifiable goals. | [221.6k](https://github.com/multica-ai/andrej-karpathy-skills) | [Install](catalog/engineering.md#karpathy-guidelines) |
<!-- END catalog -->

## Contribute

Suggest a skill using the [issue template](.github/ISSUE_TEMPLATE/suggest-skill.md), fix an upstream link, or submit a reproducible evaluation. Read [CONTRIBUTING.md](CONTRIBUTING.md) before editing the catalog. Skill data lives in [catalog/skills.yaml](catalog/skills.yaml); README tables, category pages, attribution, and review records are generated from it.

## Maintain this registry

Requires Python 3.11+.

```bash
python -m pip install -r requirements.txt
python scripts/validate_catalog.py
python -m unittest discover -s tests -v
python scripts/render_catalog.py --check
python scripts/update_stars.py --dry-run
python scripts/update_stars.py
```

Set `GH_TOKEN` or `GITHUB_TOKEN` in your environment for authenticated GitHub API access. Tokens are never stored in the catalog. A failed refresh preserves the previous snapshot and exits nonzero. The daily workflow opens or updates a pull request, subject to repository Actions settings; see [publishing and automation setup](docs/publishing.md).

## About the first release

Read the [English introduction](docs/blog/introducing-devskill-hub.md) or [中文介绍](docs/blog/introducing-devskill-hub.zh-CN.md). The first release covers the original nine category candidates plus the subsequently requested Karpathy Guidelines entry. Future work includes reproducible evaluations and broader coverage; those are not available yet.

## License & attribution

Original code and documentation use the [MIT License](LICENSE). The copyright-holder field must be filled in by the maintainer before publication. Upstream projects retain their own licenses, including file-level exceptions and incomplete licensing evidence. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Inclusion does not imply endorsement by upstream authors.
