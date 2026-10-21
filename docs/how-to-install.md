# Installation guide / 安装指南

Installation commands and source evidence are maintained per entry in [catalog/skills.yaml](../catalog/skills.yaml) and rendered into the category pages. Use those copyable blocks rather than assuming every repository supports the same installer.

各条目的命令、来源与限制由 YAML 统一维护并生成到分类页。不要假定所有仓库都支持同一个安装命令。

## Choose the entry and the agent

| Category | Copyable methods and caveats |
| --- | --- |
| Frontend / 前端 | [Frontend installation details](../catalog/frontend.md) |
| Backend / 后端 | [Backend installation details](../catalog/backend.md) |
| Database / 数据库 | [Database installation details](../catalog/database.md) |
| Engineering / 工程实践 | [Engineering installation details](../catalog/engineering.md) |

The methods differ:

- **Claude Code plugin commands** begin with `/plugin` and belong inside Claude Code. A marketplace command registers a source; a second command installs a bundle. A bundle can contain skills beyond the one listed here.
- **Shell installers** such as `npx` and `uipro` run in a terminal, generally from your project root. Node.js/npm may be required; UI/UX Pro Max also uses Python for its search tools.
- **Manual installation** must preserve the complete upstream skill directory, supporting files, and applicable license notices. Follow upstream instructions for the target agent and project/global scope.

`/plugin` 在 Claude Code 内执行；`npx`、`npm` 和 `uipro` 在终端执行。手动安装需要保留完整目录、脚本、参考资料和适用的许可证说明。项目级与全局安装路径应以上游和所用 Agent 的说明为准。

## Important upstream differences

Addy Osmani's repository warns that individual-skill installs may omit shared repository-level references. The listed command is the documented repository installation entry point; use the native integration when you need all shared checklists.

UI/UX Pro Max documents the current `ui-ux-pro-max-cli` package and the `uipro` executable. Impeccable documents its own installer and harness setup. Google's installer asks which skills, target agents, and scope to use. Karpathy's documentation still uses a legacy repository owner, which is called out in its entry.

Addy Osmani 的单 Skill 安装可能缺少共享 references。UI/UX Pro Max 的当前包名和命令名不同。Impeccable 有自己的安装器。Google 安装器会交互选择条目和目标 Agent。Karpathy 的旧仓库名称问题也在条目中单独说明。

## Verification boundary

This release reviewed the published installation instructions and inspected actual skill files. It did not run third-party installers, provision cloud resources, or test all supported agents. Compatibility claims originate upstream unless a reproducible test report is linked. If an installation breaks, report the agent/version, operating system, command, error, and upstream revision without credentials.

本版本没有执行第三方安装器、创建云资源或测试所有 Agent。安装失败时，请提供工具版本、系统、命令、错误和上游版本，删除日志中的凭据。
