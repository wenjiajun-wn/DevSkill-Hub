# Evaluation criteria / 评估标准

## Admission

A candidate needs a public upstream repository, a real `SKILL.md` with nonempty `name` and `description` frontmatter, a concrete developer use case, and traceable installation and licensing evidence. Summaries must describe inspected content. Clearly label incomplete evidence rather than treating repository existence as verification.

候选需有公开来源、有效的 `SKILL.md`、具体开发场景及可追溯的安装和许可证依据。证据不足应明确标记，不得把“仓库存在”当成“效果已验证”。

## Independent states

| YAML field | Meaning | Evidence |
| --- | --- | --- |
| `verification.metadata` | Source content and metadata inspected | Actual file, reviewed commit, file modification date, category fit, and scoped license evidence |
| `verification.installation` | Published method reviewed | Upstream documentation URL and exact command/workflow |
| `verification.installation_tested` | Installation executed successfully | A reproducible installation report, agent/version, OS, scope, and source revision |
| `verification.effectiveness` | A task-level evaluation completed | `test_report_url`, task, acceptance criteria, agent/model version, source revision, output, limitations |

`false` means no qualifying evidence is recorded; it does not mean the skill is defective. The initial catalog has content and installation-documentation reviews, with installation execution and effectiveness left false. “Metadata reviewed” can coexist with incomplete license evidence if that incompleteness is explicitly recorded, as in the Karpathy entry. Such a declaration is not a claim of a complete redistribution license.

`false` 表示没有相应证据，并不表示 Skill 有问题。元数据审查允许记录“不完整的许可证证据”，但必须公开说明，不能据此声称可无条件再分发。

## Ranking and freshness

Sort categories in the order declared in the schema. Within each category sort by repository stars descending, with null values last and skill IDs ascending for ties. Shared repositories have one shared snapshot. Stars are repository-level popularity, not skill ratings.

`stars_updated_at` records a successful API observation. `verification.last_reviewed` records content review. `skill_updated_at` records the latest commit affecting the skill path. Repository `updated_at` and `pushed_at` are separate activity fields captured during review. Daily star refreshes must not renew content-review claims.

按来源仓库 Star 降序展示，未知值排末尾，同分按 ID 升序。Star 采集、内容审查、文件修改和仓库活动是四种不同时间，不能混用。

## Suggested future evaluation

Before claiming effectiveness, define a small task and acceptance criteria, record the environment, and preserve enough output to reproduce the result. Compare the skill-assisted result with an appropriate baseline, disclose failures, and review any generated changes. These evaluations are planned work; this release does not include a benchmark suite.
