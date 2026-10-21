# Introducing DevSkill Hub: A Curated Collection of Developer Agent Skills

An AI coding assistant can write code quickly and still miss the work around it: choosing an API contract, making a component accessible, or agreeing on what a business term means. Repeating those expectations in every conversation is tedious. Agent Skills offer a way to capture them once and bring them into a task when they are useful.

## From prompts to reusable practices

A skill is a small package built around a `SKILL.md` file. It describes when the agent should use it and how to approach a particular kind of work. Some packages are mostly instructions. Others include references, examples, or scripts that the agent can run. The [Agent Skills specification](https://agentskills.io/specification) describes the common structure.

For developers, the value is repeatability. A team can use an API review workflow that asks about compatibility, or a frontend workflow that treats keyboard navigation as part of implementation. Skills supplement project context and human review; they do not guarantee correct output.

## The discovery problem

The ecosystem is spread across personal repositories, vendor examples, and larger collections. A promising repository title does not tell you where the actual skill lives, which installer is supported, or whether an advertised capability has been tested. A repository's popularity can also hide differences between the skills it contains.

DevSkill Hub starts with a narrow response to that problem: a curated registry with original summaries, category pages, direct upstream links, documented installation methods, and explicit verification states. We link to upstream content rather than copying entire skills into another repository.

## The first selection

The original brief called for nine skills: four frontend, three backend, and two database entries. A subsequent request added Karpathy Guidelines as a tenth entry in Engineering Practices. The current selection is:

<!-- BEGIN edition-list -->
- **Frontend Development**: [Frontend Design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md), [Frontend UI Engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/frontend-ui-engineering/SKILL.md), [Impeccable](https://github.com/pbakaus/impeccable/blob/main/.agents/skills/impeccable/SKILL.md), [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/.claude/skills/ui-ux-pro-max/SKILL.md).
- **Backend Development**: [API and Interface Design](https://github.com/addyosmani/agent-skills/blob/main/skills/api-and-interface-design/SKILL.md), [API Design Reviewer](https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skills/api-design-reviewer/SKILL.md), [Domain Modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md).
- **Database Development**: [Cloud SQL Basics](https://github.com/google/skills/blob/main/skills/cloud/cloud-sql-basics/SKILL.md), [Database Designer](https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skills/database-designer/SKILL.md).
- **Engineering Practices**: [Karpathy Guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md).
<!-- END edition-list -->

The selection spans visual direction, component engineering, domain language, API contracts and reviews, schema design, managed cloud databases, and disciplined code changes. These are editorial choices for a focused first release, not a claim that they are the best options for every team.

## What “verified” means here

For each entry, we inspected its actual `SKILL.md`, upstream installation documentation, license evidence, and category fit. We recorded a reviewed source revision and the latest commit affecting that file. Repository stars come from the GitHub API and are sorted within each category.

That does not establish installation success or practical effectiveness. The catalog tracks those states separately and currently makes neither claim. This distinction also exposes incomplete information: Karpathy Guidelines declares MIT but lacks a root LICENSE file, and its README still uses a legacy repository owner in installation commands. Those facts belong beside the entry, not behind an unqualified verification badge.

The [verification record](../verification.md) explains the path corrections and limitations. Stars are repository-level snapshots; they are neither per-skill ratings nor a substitute for evaluation.

## Find a skill and try it

Start from the [catalog in the README](../../README.md#frontend), choose the task you need help with, and open its installation instructions. Use the upstream method for your agent. Some entries install bundles rather than a single skill, and some need supporting scripts or reference directories.

For a first trial, choose a small change with a clear success criterion: improve keyboard navigation in a component, compare two API contracts, or clarify an ambiguous domain term. Inspect the generated code and run the relevant checks. Keep the skill if it improves that workflow in your context.

## Keeping the registry maintainable

The source of truth is [catalog/skills.yaml](../../catalog/skills.yaml). Repository metadata is stored once even when several entries share a source. A Python validator checks structure, evidence fields, IDs, links, and ordering. A renderer keeps the README tables and category pages synchronized. Unit tests exercise sorting and API failure handling.

A daily GitHub Actions workflow refreshes repository stars and proposes changes through a pull request. It requires the host repository's Actions permissions to be configured after publication. It does not automatically renew the content-review date or certify that a changed upstream skill still works.

## What comes next

Future work should make quality claims more useful: reproducible evaluation tasks, installation smoke tests in disposable environments, and a documented review cadence. Broader coverage can follow when a candidate has a clear use case and verifiable upstream evidence. These are roadmap items, not released features.

The most useful contribution today may be a corrected path, an installation caveat, or a small task with a reproducible outcome. Read [the contribution guide](../../CONTRIBUTING.md), share the source evidence, and help keep the directory accurate.
