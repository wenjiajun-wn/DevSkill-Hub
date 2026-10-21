# Functional smoke evaluations / 功能冒烟评估

Installation and usefulness are separate questions. We executed selected bundled tools against original fixtures, and conducted explicitly labeled manual walkthroughs for instruction-led skills. These are bounded observations, not a controlled benchmark, an automatic agent-activation test, or proof of improvement over an unassisted baseline.

已实际运行有配套工具的条目，并为说明型 Skill 记录限定范围的人工演练。没有开展对照模型实验、浏览器视觉评测或云资源部署，不能据此保证生产效果。`verification.effectiveness` remains false until a qualifying task-level model evaluation is recorded; smoke evidence has a separate scope field.

## Reproduce executable checks

First run the [installation tests](installation-smoke.md). Then:

```bash
python scripts/smoke_functionality.py
```

The default command fails when an acceptance check fails. To explicitly accept only the documented upstream SQL-parser limitation while requiring the JSON alternative and all other checks to pass:

```bash
python scripts/smoke_functionality.py --allow-known-limitations
```

See [machine-readable observations](functionality.json). Tool output and temporary source files remain under ignored `.cache/`; this repository distributes original fixtures and concise observations only.

<a id="ui-ux-pro-max"></a>

## UI/UX Pro Max

Task: retrieve actionable guidance for keyboard focus. Executed the installed `scripts/search.py` with `keyboard focus visible`, domain `ux`, JSON output. Acceptance: at least one result explicitly addresses focus. Observation: three relevant results; passed. This checks retrieval with packaged data, not the quality of a generated interface.

<a id="api-design-reviewer"></a>

## API Design Reviewer

Task: flag inconsistent REST resource naming, then detect removal of an endpoint. Used an original OpenAPI document containing `/getUsers`, followed by a version with that path removed. Acceptance: naming findings and a breaking-change result with the documented nonzero gate. Observations: nine lint findings; one breaking change; detector exit 1. Both passed. Linter exit 0 alone does not mean a clean API; its JSON findings must be inspected.

<a id="database-designer"></a>

## Database Designer — limitation found

Task: analyze two linked tables in [schema.sql](fixtures/schema.sql), expecting two tables and one foreign key. The fixture was executed in an in-memory SQLite database and `PRAGMA foreign_key_list` confirmed the relationship. The installed analyzer reported two tables but **zero foreign keys** and also flagged a NOT NULL column as nullable. This SQL input did not meet acceptance criteria. We have not modified upstream code or presented this as a successful SQL analysis.

The same explicit structure in [schema.json](fixtures/schema.json) is a tested alternative: the analyzer reports one foreign key and generates its relationship in the ERD. Prefer the structured input for this tool and cross-check schema facts against the database engine. This does not establish that arbitrary SQL parsing is correct or validate live migrations/index performance.

SQL 输入实测暴露上游解析缺陷，已在目录中标明；结构化 JSON 输入通过对应检查。不能仅凭该工具对 SQL 文本的结果决定生产迁移。

<a id="impeccable"></a>

## Impeccable

Task: detect UI anti-patterns in an intentionally weak [HTML fixture](fixtures/problematic-ui.html). Executed the installed 4.7.0 npm CLI and its native detector with `detect --json --no-config`. Acceptance: gradient text is detected and findings use exit 2. Observation: four findings, including gradient text; passed. Static detector heuristics are not an accessibility conformance audit or a rendered visual review.

## Instruction-led skills

These six records are manual applications/reviews by the Codex assistant in this maintenance session. They do not involve separate model runs, reproducible model inference, or independent reviewers. They are kept separate from executable tool checks and do not flip the effectiveness flag.

<a id="frontend-design"></a>

### Frontend Design

Scenario: define a visual direction for a small developer registry. A suitable direction must start from the task—comparing skills and checking evidence—with readable source/installation links, restrained typography, and prominence for verification limits. The existing Markdown list uses clear category tables and direct source links rather than introducing decorative cards or motion into a GitHub reading surface. Reviewed outcome: appropriate direction for this repository; no claim about generated web UI or rendered typography. No browser experiment was conducted.

<a id="frontend-ui-engineering"></a>

### Frontend UI Engineering

Scenario: specify an accessible future skill-filter component. Acceptance criteria: labeled native search input, a button with visible text, keyboard reachability, one clear result heading, and loading/empty/error states that convey actionable text. The walkthrough rejects clickable divs, color-only verification states, and a global store for a local filter. Outcome: a concrete acceptance checklist for future UI implementation; no component was shipped or browser-tested, so effectiveness remains untested.

<a id="domain-modeling"></a>

### Domain Modeling

Applied the installed instruction to this registry's vocabulary: distinguish a skill entry from its source repository; an observation from a content review; installation documentation from installation execution; and missing stars from zero stars. The edge case of two skills from the same repository resolves to one shared repository snapshot. The resulting [glossary](../../GLOSSARY.md) and [decision record](../adr/0001-repository-metadata.md) capture the decisions. This is a reviewed documentation outcome, not a comparative model evaluation.

<a id="api-and-interface-design"></a>

### API and Interface Design

Applied boundary validation and explicit failure semantics to the upstream checker: incomplete GitHub trees and malformed responses fail instead of producing a false “unchanged” report; identical trees produce stable reports; changes do not mutate the review baseline. These behaviors are exercised in `tests/test_upstreams.py`. This verifies the project's API consumer contract; it does not benchmark the skill's ability to design arbitrary REST services.

<a id="karpathy-guidelines"></a>

### Karpathy Guidelines

Applied explicit success criteria and focused edits to the real multi-file write bug. The acceptance criteria are byte-for-byte restoration after a replacement failure, recovery after interruption, and serialization of writers. The regression cases in `tests/test_transaction.py` pass. This session demonstrates a concrete workflow and tested code outcome, without claiming that the skill caused improvement over a baseline.

<a id="cloud-sql-basics"></a>

### Cloud SQL Basics

Scenario: explain a PostgreSQL Cloud SQL deployment to a developer before provisioning. The walkthrough identifies the target project/region and database engine; API enablement and appropriate IAM permissions; instance/database/user separation; backup and recovery requirements; and a secure connector or Auth Proxy connection rather than an unrestricted public endpoint. It distinguishes managed MySQL, PostgreSQL, and SQL Server. Secrets must be supplied at runtime rather than committed. Outcome: an offline explanation consistent with the installed references. No Google Cloud credentials, instance, billable operation, backup restore, or network connectivity was tested.

## How to interpret this release

All ten entries have installation smoke evidence. Four entries have executable tool observations, including the database limitation. Six have documented instruction walkthroughs. **No entry is advertised as having proven comparative effectiveness.** Future contributors can attach reproducible task/model/environment evidence under the existing effectiveness criteria.
