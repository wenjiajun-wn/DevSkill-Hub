# 我为什么决定开源 DevSkill Hub：打造高质量开发 Agent Skills 精选库

AI 编程助手能很快写出代码，但开发工作并不止于“把代码写出来”。一个接口要考虑兼容性，一个组件要支持键盘操作，一段业务逻辑背后还可能藏着没有对齐的领域概念。如果每次对话都重新解释这些要求，既重复，也容易遗漏。

Agent Skills 提供了一种把工作方法沉淀下来的方式。DevSkill Hub 则希望先解决使用它们之前的一步：去哪里找，以及如何判断一个 Skill 是否适合当前任务。

## Agent Skills 是什么？

一个 Skill 通常以 `SKILL.md` 为入口，说明它适合什么任务，以及 Agent 应如何开展工作。有些包主要是方法说明，有些还包含参考资料、示例和配套脚本。[Agent Skills 规范](https://agentskills.io/specification)定义了常见结构。

对开发者来说，关键在于复用。例如，可以把 API 兼容性检查变成固定的审查步骤，也可以让无障碍要求在组件开发时就进入流程。Skill 仍然需要项目背景、测试和人的判断，不能保证输出正确。

## 为什么还需要一个精选目录？

目前的资源分散在个人仓库、厂商示例和大型集合中。看到一个名字很合适的项目，并不意味着已经知道实际 Skill 的位置、支持的安装方法和配套依赖。仓库很热门，也不能说明其中每一个条目都适合自己的场景。

因此，第一版的目标很克制：建立有分类、有来源、有安装依据、有核查记录的精选目录。我们编写原创简介，链接到上游，不把第三方完整 Skill 再复制一份。

## 第一版收录了什么？

最初的范围是九个 Skills：前端四个、后端三个、数据库两个。随后根据追加需求，将 Karpathy Guidelines 放入“工程实践”，总计十个条目：

<!-- BEGIN edition-list -->
- **前端开发**: [Frontend Design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md), [Frontend UI Engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/frontend-ui-engineering/SKILL.md), [Impeccable](https://github.com/pbakaus/impeccable/blob/main/.agents/skills/impeccable/SKILL.md), [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/.claude/skills/ui-ux-pro-max/SKILL.md).
- **后端开发**: [API and Interface Design](https://github.com/addyosmani/agent-skills/blob/main/skills/api-and-interface-design/SKILL.md), [API Design Reviewer](https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skills/api-design-reviewer/SKILL.md), [Domain Modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md).
- **数据库开发**: [Cloud SQL Basics](https://github.com/google/skills/blob/main/skills/cloud/cloud-sql-basics/SKILL.md), [Database Designer](https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skills/database-designer/SKILL.md).
- **工程实践**: [Karpathy Guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md).
<!-- END edition-list -->

这些条目分别覆盖视觉方向、组件工程、领域术语、API 契约与审查、数据库结构、云数据库和编码行为规范。这是第一版的编辑选择，不表示它们在任何团队中都优于其他方案。

## “已验证”需要说清楚

本次核查阅读了实际 `SKILL.md`、上游安装说明和许可证依据，检查功能是否符合分类，并记录来源版本与文件最后修改时间。Star 来自 GitHub API，在各类别内部按来源仓库排序。

这些检查不能直接证明安装成功，更不能证明能提高真实项目的产出质量。因此，目录分别记录“元数据已审查”“安装说明已审查”“安装已执行”和“效果已测试”。目前没有宣称后两项已经完成。

不完整的信息也应当公开。例如，Karpathy Guidelines 在 frontmatter 和 README 中声明 MIT，但没有根目录 LICENSE；安装命令仍使用旧所有者名称。这些限制会写入条目和[核查记录](../verification.md)，不会被一个笼统的“已验证”徽章掩盖。

Star 是整个来源仓库的快照，不是单个 Skill 的独立得分，也不是效果评测。

## 如何查找和安装？

从 [README 目录](../../README.zh-CN.md#frontend)找到当前任务对应的分类，打开条目的安装说明，再按自己的 Agent 选择上游方法。部分方法安装的是插件包，部分 Skill 还依赖脚本或共享参考资料，不能只复制一个 Markdown 文件就认为安装完成。

第一次尝试可以选一个小任务：修复组件键盘操作、比较两个接口版本，或澄清一个存在歧义的业务术语。先定义成功标准，再审查输出、运行检查，观察它是否改善了自己的工作流程。

## 怎样持续维护？

[catalog/skills.yaml](../../catalog/skills.yaml)是唯一数据源。同一来源仓库的信息只保存一份。Python 校验脚本检查结构、证据字段、ID、链接与排序，生成脚本同步更新 README 和分类页，单元测试覆盖排序和 API 失败等核心逻辑。

每天运行的 GitHub Actions 会刷新 Star，并通过 PR 提交变更；发布后需要仓库允许 Actions 创建 PR。Star 自动更新不会顺带刷新内容审查时间，也不会自动证明上游变更后的 Skill 依旧有效。

## 后续计划

下一步应当让质量判断更有依据：建立可复现的评估任务，在可丢弃环境里进行安装冒烟测试，并明确内容复审周期。更多领域的收录也应以清晰用途和可核实来源为前提。这些都还是路线图，当前版本尚未提供。

现在就能参与的贡献包括修正路径、补充安装限制，以及提供一个记录结果的小任务。欢迎阅读[贡献指南](../../CONTRIBUTING.md)，带上可追溯的来源，一起把这个目录维护准确。
