# Maintenance validation record

Follow-up validation performed on 2026-10-21 for DevSkill Hub v0.1.0. The initial release had 39 tests; the follow-up adds regression coverage and actual installation/tool observations.

| Check | Result |
| --- | --- |
| Runtime | Python 3.13.13; PyYAML 6.0.3; Node.js 22.23.1 |
| Catalog | 10 skills, 8 source repositories; original 4 / 3 / 2 entries plus 1 engineering entry |
| Schema, ordering, evidence fields | `python scripts/validate_catalog.py` passes |
| Generated documentation | `python scripts/render_catalog.py --check` passes |
| Offline unit tests | 51 tests pass with `python -m unittest discover -s tests -v` |
| Multi-file writes | Failure rollback, new-file removal, interrupted-write recovery, committed-journal handling, recovery retry, and writer serialization covered |
| Live star refresh | Updated YAML and all generated pages with the recoverable transaction writer |
| Upstream monitoring | 8 live repository trees checked against recorded directory/file hashes; no monitored drift at the follow-up check |
| Installation execution | All 10 entries passed installed-file identity and supporting-resource checks in isolated Windows projects |
| Functional tools | UI retrieval, API linting/breaking-change detection, JSON schema analysis, and Impeccable detection executed |
| Known upstream defect | SQL schema analyzer missed a foreign key confirmed by SQLite; the equivalent JSON input passed |
| Hosted validation | [Follow-up validation run](https://github.com/wenjiajun-wn/DevSkill-Hub/actions/runs/39561788481) passed on the repair commit with Python 3.11 and 3.13 |
| Star-update automation | [Initial run](https://github.com/wenjiajun-wn/DevSkill-Hub/actions/runs/39556064054) created [PR #1](https://github.com/wenjiajun-wn/DevSkill-Hub/pull/1); [follow-up run](https://github.com/wenjiajun-wn/DevSkill-Hub/actions/runs/39561874058) passed and updated that same PR |
| Upstream-monitor automation | [Hosted upstream-check run](https://github.com/wenjiajun-wn/DevSkill-Hub/actions/runs/39561879272) passed; unchanged content produced no extra review PR |
| Bot update branch | [Manual validation of the bot branch](https://github.com/wenjiajun-wn/DevSkill-Hub/actions/runs/39562277004) passed on the exact PR head |

Read the [installation evidence](evaluations/installation-smoke.md), [functional scope and limitations](evaluations/functional-smoke.md), [upstream report](upstream-status.md), and [verification records](verification.md). Star timestamps and values are maintained in [catalog/skills.yaml](../catalog/skills.yaml), independently of content reviews.

## Recovery semantics

The maintenance tools take one writer lock, stage the entire batch, and journal original file contents before replacements. A normal failure rolls back changed files. If restoration itself is blocked, backups and the journal are retained and the command fails with recovery instructions. After a hard process interruption the next maintenance run restores the old batch, or preserves a batch whose commit marker was already recorded. Individual replacements are atomic; independent readers can briefly see intermediate files. No claim of a filesystem-wide atomic transaction or guaranteed recovery after storage loss is made.

## Boundaries and project decisions

- The verified GitHub owner handle `wenjiajun-wn` fills the MIT copyright attribution.
- The maintainer explicitly chose not to add a private reporting contact. The code of conduct uses GitHub's content-reporting route and does not treat a missing contact as unfinished work.
- Karpathy's canonical repository address successfully installed. Its README/frontmatter declare MIT, but a complete root LICENSE remains absent; this is explicitly marked as declaration-only evidence. No upstream license was fabricated or modified.
- Installation smoke checks do not prove automatic model activation or comparative usefulness. Four entries have executable helper-tool observations; six have labeled manual walkthroughs. No comparative effectiveness flag has been set true.
- No paid model sessions or cloud resources were provisioned. Cloud SQL was installed and reviewed offline; live cloud connectivity, backups, and recovery remain outside the recorded test scope.
- Upstream drift detection proposes review findings. It does not silently reset hashes, renew review claims, approve PRs, or merge changes.
- GitHub placed the bot-created `pull_request` validation event in an approval-required state. The maintenance job had already run checks before creating/updating its PR, and a separate manual validation on the same PR head passed. PR review and merge remain manual.
- Temporary upstream source files and installer caches are ignored by Git and excluded from publication. The repository contains original fixtures, summaries, and sanitized observations.
