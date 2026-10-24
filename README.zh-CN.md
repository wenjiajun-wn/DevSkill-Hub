# DevSkill Hub

**Discover, Install, and Master the Best Developer Agent Skills.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[English](README.md) · 简体中文

一个专注于 AI Coding 的开发者 Agent Skills 精选目录，覆盖前端、后端、数据库和通用工程实践，帮助使用 Codex、Claude Code、Cursor 等工具的开发者发现、了解和安装适合任务的 Skills。

<!-- BEGIN summary -->
**v0.1.0 · 10 个 Skills · 8 个来源仓库**

前端开发 4 / 后端开发 3 / 数据库开发 2 / 工程实践 1

10 个条目通过隔离安装冒烟检查；[实测范围与限制](docs/evaluations/functional-smoke.md)包含已发现的上游缺陷。
<!-- END summary -->

[前端](#frontend) · [后端](#backend) · [数据库](#database) · [工程实践](#engineering) · [开始使用](docs/getting-started.md) · [参与贡献](CONTRIBUTING.md)

## 为什么做这个目录？

Agent Skills 以 `SKILL.md` 为入口，将任务说明、参考资料和可选工具组织成可复用的工作方法。例如，它们可以指导 Agent 实现无障碍组件、审查 API 或讨论领域模型。

有用的 Skills 分散在不同仓库，路径、安装方式和许可证也会变化。这个项目把这些信息整理到一起，提供来源、审查记录和明确的验证状态。第一阶段采用外部链接索引，不复制第三方完整 Skill 或脚本。

## 快速开始

1. 在下方目录中找到适合任务的 Skill，点击“安装”查看上游方法和注意事项。
2. 阅读来源文件，按所用 Agent 的安装说明操作。“命令有文档依据”与“安装已实测”是不同状态。
3. 在一个可审查的小任务中尝试，检查输出后再扩大使用范围。

<!-- BEGIN quick-install -->
例如，上游提供以下安装入口 ([来源](https://github.com/addyosmani/agent-skills#quick-start)):

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```
<!-- END quick-install -->

这会安装包含多个 Skill 的插件包。请先阅读[安装指南](docs/how-to-install.md)，尤其是上游关于单 Skill 安装可能缺少共享参考资料的说明。`/plugin` 命令在 Claude Code 内输入；隔离安装实测使用等价的原生 CLI，并指定项目范围。

## 如何理解验证状态？

- **元数据已审查**：检查实际 `SKILL.md`、分类适用性、来源版本、许可证依据及上游说明。
- **安装说明已审查**：上游文档包含对应方法；另设“安装已执行”字段记录实测。
- **效果已测试**：需要记录具体任务和结果。当前条目都没有作此声明。

参见[评估标准](docs/evaluation-criteria.md)和[上游核查记录](docs/verification.md)。Star 只是来源仓库的受欢迎程度，不能替代质量评测。

<!-- BEGIN catalog -->
Star 数据采集时间（UTC）：**2026-10-24T08:07:52Z**。

Stars 属于来源仓库；它不是单个 Skill 的评分，也不代表实际效果。N/A 表示没有已验证数据。

<a id="frontend"></a>

## 前端开发

| 排名 | Skill | 简介 | 仓库 Stars | 安装 |
| ---: | --- | --- | ---: | --- |
| 1 | [Frontend Design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | 指导有辨识度的视觉风格、字体排版与界面设计。 | [183.4k](https://github.com/anthropics/skills) | [安装](catalog/frontend.md#frontend-design) |
| 2 | [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/.claude/skills/ui-ux-pro-max/SKILL.md) | 提供可检索的配色、字体、无障碍与多技术栈界面设计指导。 | [139.6k](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | [安装](catalog/frontend.md#ui-ux-pro-max) |
| 3 | [Frontend UI Engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/frontend-ui-engineering/SKILL.md) | 涵盖组件架构、响应式布局、状态管理与无障碍界面。 | [110.0k](https://github.com/addyosmani/agent-skills) | [安装](catalog/frontend.md#frontend-ui-engineering) |
| 4 | [Impeccable](https://github.com/pbakaus/impeccable/blob/main/.agents/skills/impeccable/SKILL.md) | 通过设计工作流审查、评议、打磨界面并完善动效。 | [85.7k](https://github.com/pbakaus/impeccable) | [安装](catalog/frontend.md#impeccable) |

<a id="backend"></a>

## 后端开发

| 排名 | Skill | 简介 | 仓库 Stars | 安装 |
| ---: | --- | --- | ---: | --- |
| 1 | [Domain Modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md) | 澄清领域术语、推敲边界场景，并维护术语表与架构决策记录。 | [302.0k](https://github.com/mattpocock/skills) | [安装](catalog/backend.md#domain-modeling) |
| 2 | [API and Interface Design](https://github.com/addyosmani/agent-skills/blob/main/skills/api-and-interface-design/SKILL.md) | 指导契约优先的接口设计、兼容性、边界校验与错误语义。 | [110.0k](https://github.com/addyosmani/agent-skills) | [安装](catalog/backend.md#api-and-interface-design) |
| 3 | [API Design Reviewer](https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skills/api-design-reviewer/SKILL.md) | 结合检查工具审查 REST 规范、OpenAPI 契约与破坏性变更。 | [28.6k](https://github.com/alirezarezvani/claude-skills) | [安装](catalog/backend.md#api-design-reviewer) |

<a id="database"></a>

## 数据库开发

| 排名 | Skill | 简介 | 仓库 Stars | 安装 |
| ---: | --- | --- | ---: | --- |
| 1 | [Database Designer](https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skills/database-designer/SKILL.md) | 辅助 Schema 建模、索引分析、关系设计和迁移规划。 | [28.6k](https://github.com/alirezarezvani/claude-skills) | [安装](catalog/database.md#database-designer) |
| 2 | [Cloud SQL Basics](https://github.com/google/skills/blob/main/skills/cloud/cloud-sql-basics/SKILL.md) | 指导 Cloud SQL 实例、数据库、备份、可用性与安全连接。 | [21.5k](https://github.com/google/skills) | [安装](catalog/database.md#cloud-sql-basics) |

<a id="engineering"></a>

## 工程实践

| 排名 | Skill | 简介 | 仓库 Stars | 安装 |
| ---: | --- | --- | ---: | --- |
| 1 | [Karpathy Guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md) | 通过明确假设、保持简单、聚焦修改与可验证目标减少编码错误。 | [223.0k](https://github.com/multica-ai/andrej-karpathy-skills) | [安装](catalog/engineering.md#karpathy-guidelines) |
<!-- END catalog -->

## 参与贡献

欢迎通过 [Issue 模板](.github/ISSUE_TEMPLATE/suggest-skill.md)推荐 Skill、修复信息或提交可复现的评估。修改前请阅读[贡献指南](CONTRIBUTING.md)。所有条目数据维护在 [catalog/skills.yaml](catalog/skills.yaml)，README 表格、分类页、来源声明和审查记录由脚本同步生成。

## 本地维护

需要 Python 3.11 或更高版本。

```bash
python -m pip install -r requirements.txt
python scripts/validate_catalog.py
python -m unittest discover -s tests -v
python scripts/render_catalog.py --check
python scripts/update_stars.py --dry-run
python scripts/update_stars.py
```

认证访问 GitHub API 时，在环境变量中设置 `GH_TOKEN` 或 `GITHUB_TOKEN`。Token 不写入目录。一次刷新只要有仓库请求失败，就保留原快照并以非零状态退出。每天运行的工作流会创建或更新 PR，需要仓库允许 Actions 创建 PR；详见[发布与自动化设置](docs/publishing.md)。

## 关于第一版

阅读[中文介绍](docs/blog/introducing-devskill-hub.zh-CN.md)或[英文介绍](docs/blog/introducing-devskill-hub.md)。第一版包含原定的九个分类候选，以及后续加入的 Karpathy Guidelines。目前已有[安装与功能冒烟证据](docs/evaluations/installation-smoke.md)，对照模型评估和更多分类仍属于后续计划。

## 许可证与署名

本项目原创代码和文档使用 [MIT License](LICENSE)，署名为已核实的仓库所有者 `wenjiajun-wn`。第三方项目保留各自许可证，包括文件级例外及证据不完整的情况；详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。收录不代表上游作者对本项目的官方认可。
