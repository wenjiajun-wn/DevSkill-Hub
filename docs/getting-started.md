# Getting started / 开始使用

DevSkill Hub is a directory, not an installer or a bundle of vendored skills. You do not need Python to browse it. Python is needed only to maintain this repository.

本项目是精选目录。浏览和查找 Skill 不需要 Python；只有维护目录时才需要 Python。

1. Start with a concrete task: a UI review, API contract, business vocabulary, or database design.
2. Browse [Frontend](../catalog/frontend.md), [Backend](../catalog/backend.md), [Database](../catalog/database.md), or [Engineering Practices](../catalog/engineering.md).
3. Read the entry's source, use cases, license caveat, verification states, and installation notes.
4. Follow the [installation guide](how-to-install.md), then test the skill on a small, reviewable task.

先明确任务，再阅读分类页的适用场景、来源、许可证与验证状态，按上游方法安装。第一次使用应当选择范围小、结果可审查的任务。

## Example: review an API change

Choose **API and Interface Design** if you are defining contracts and compatibility expectations. Choose **API Design Reviewer** if you need to compare OpenAPI documents and inspect the supplied review tools. Open each upstream `SKILL.md` before use; neither has been benchmarked by this registry.

设计接口契约可以先了解 API and Interface Design；需要比较 OpenAPI 文档和检查工具时，可以了解 API Design Reviewer。它们的安装说明经过核查，但实际效果尚未由本目录测试。

## What to check after installation

Confirm that your agent discovers the intended skill, that its scripts/references are present, and that any prerequisites are available. Restart or reload the agent when upstream instructs you to do so. Compare the output against a concrete acceptance criterion and run your project's normal checks.

检查 Agent 能否发现 Skill、脚本与参考资料是否完整、依赖是否满足；需要时重新加载。使用具体验收标准和项目检查评估结果。

Read [evaluation criteria](evaluation-criteria.md) for what this directory does and does not verify, and [verification records](verification.md) for known upstream differences.
