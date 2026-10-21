# Contributing to DevSkill Hub

Thank you for helping keep this directory accurate. English and Chinese contributions are welcome. Follow our [code of conduct](CODE_OF_CONDUCT.md).

## Suggest a skill

Use the [suggestion template](.github/ISSUE_TEMPLATE/suggest-skill.md). Supply a public repository, exact `SKILL.md` URL, useful developer task, license evidence, and upstream installation instructions. Repository stars help order entries, not decide quality. Read the [evaluation criteria](docs/evaluation-criteria.md).

We index links and write original summaries. Do not copy third-party skill bodies, scripts, or repositories into this project. When licensing is incomplete, preserve the evidence and explicitly state what is unknown; do not infer permission from public availability.

## Edit the catalog

All entry data belongs in [catalog/skills.yaml](catalog/skills.yaml). The normalized structure is:

- `schema_version` and project `version` describe the catalog schema and release.
- `categories` defines the four category labels in display order.
- `repositories` is keyed by `owner/repository`. Store `url`, `default_branch`, repository-level `stars`, `stars_updated_at`, reviewed `updated_at`/`pushed_at`, scoped `license` evidence and `monitoring` once. License `evidence_status` distinguishes `license-file-reviewed` from `declaration-only`. Monitoring stores `reviewed_at` and `files` (path to Git blob/tree SHA, or null for an expected-missing path).
- `skills` references a repository key. Each entry needs a stable kebab-case `id`, display `name`, `category`, English/Chinese summaries and use cases, `tags`, actual `skill_path`/`skill_url`, `upstream_name`, reviewed `source_commit`, `skill_updated_at`, `install`, `verification`, and review notes in both languages.

Use an existing entry as the complete example. For unverified facts use null, not a guessed path, zero stars, or an invented command. A missing star count requires a null observation timestamp. An unreviewed installation command must be null. `verification.metadata`, `installation`, `installation_tested`, and `effectiveness` are separate booleans. Keep claims proportional to the evidence.

Supported categories are `frontend`, `backend`, `database`, and `engineering`. Adding a new category requires updating the shared schema, documentation, and relevant tests. More skills within a category do not require hard-coded count changes.

Preserve the original review date unless you actually recheck content. Update both source links and recorded paths when upstream reorganizes files, describe the correction in the review notes, and rerun the renderer. Repository star refreshes alone must not mark installation or effectiveness as tested.

## Local checks

Use Python 3.11+ in a virtual environment:

```bash
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` in a POSIX shell, then run:

```bash
python -m pip install -r requirements.txt
python scripts/validate_catalog.py
python scripts/render_catalog.py
python scripts/render_catalog.py --check
python scripts/check_links.py
python -m unittest discover -s tests -v
```

Sort entries after changing star metadata with the updater, or use `sort_skills` from `scripts.catalog` when editing offline. It groups by category, sorts known repository stars descending, places null last, and breaks ties by ID. Never fabricate a live observation to satisfy ordering.

Do not manually edit generated category pages, third-party notices, verification records, or marked sections in READMEs/blogs. Edit YAML and regenerate them. Editorial prose outside generated markers is maintained normally.

## Star refreshes

```bash
python scripts/update_stars.py --dry-run
python scripts/update_stars.py
```

Use `GH_TOKEN` or `GITHUB_TOKEN` through the environment if needed. Do not paste tokens into YAML, issues, test fixtures, or command history. A failed refresh exits nonzero before writing data. Previous values and timestamps remain intact. Successful refreshes update timestamps even when counts do not change.

## Pull requests

1. Work on a branch in your fork or local checkout.
2. Keep the change focused and include upstream evidence and any caveats.
3. Run the local checks and include relevant results in the PR description.
4. Explain whether you reviewed documentation, executed an installation, or tested a real task.

For an installation execution claim, set `installation_test_report_url` in `verification` to a public reproducible report. Record bounded `smoke_scope` and `smoke_report_url` separately from effectiveness. Effectiveness claims require `test_report_url`. Reports should identify source revision, agent/version, environment, exact procedure, outcome, and limitations. Maintainers review claims before merging.

## Recovery and upstream monitoring

Maintenance writers share a cross-platform lock. They stage all outputs and retain a recovery journal before replacing catalog/pages. Ordinary replacement failures roll back the batch. An interrupted process is recovered before the next maintenance read/write; do not delete `.cache/catalog-transaction` when recovery is pending. Resolve disk permissions/space and rerun `python scripts/render_catalog.py`. Replacements are atomic per file, not simultaneous across unrelated filesystem readers.

Run `python scripts/check_upstreams.py --fail-on-drift` to detect changes in monitored skill directories, installation/plugin metadata, and licensing evidence. The weekly workflow proposes a report only when its contents change. Review upstream changes, rerun relevant smoke checks, then update the YAML baseline and review date in a PR. Never reset hashes merely to silence a warning.

Installation and tool-smoke reproduction commands live in [the installation report](docs/evaluations/installation-smoke.md) and [functional report](docs/evaluations/functional-smoke.md). These network-dependent tests are separate from the fast offline unit-test suite.

## 中文说明

欢迎推荐条目、修正上游路径、补充安装限制和提交可复现评估。数据只改 YAML，再生成页面。不要复制第三方完整内容，不要猜测 Star、路径或命令。PR 中请区分“读过安装说明”“执行过安装”和“评估过效果”，并给出对应证据。
