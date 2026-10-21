# Publishing and automation setup / 发布与自动化

The project has been prepared locally. No remote repository, push, or release is created by the maintenance scripts. The intended GitHub repository name is `DevSkill-Hub`; the local folder name can remain different.

本项目在当前目录完成本地准备。维护脚本不会创建远程仓库、推送或发布 Release。建议远程仓库名为 `DevSkill-Hub`，本地目录可以保留现有名称。

## Before publication

1. Confirm the copyright-holder field in [LICENSE](../LICENSE), currently the verified repository-owner handle `wenjiajun-wn`.
2. Review [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md). This project deliberately does not provide a separate private reporting contact; GitHub's content-reporting route remains available.
3. Review the [verification record](verification.md) and [installation/functional smoke evidence](evaluations/installation-smoke.md), including Karpathy's incomplete license evidence and the database SQL-parser limitation. Comparative model effectiveness remains untested.
4. Run the checks below. Consider refreshing stars if the snapshot is old.

```bash
python -m pip install -r requirements.txt
python scripts/validate_catalog.py
python scripts/render_catalog.py --check
python scripts/check_links.py
python -m unittest discover -s tests -v
```

## Create and publish when ready

The following are **manual publication instructions**, not commands automatically run by this project. If this directory is not yet a Git repository:

```bash
git init -b main
git add .
git commit -m "feat: introduce DevSkill Hub v0.1.0"
```

Create an empty public repository named `DevSkill-Hub` in your GitHub account or organization, without an initial README/license/gitignore. Add its actual clone URL (replace `YOUR_ACCOUNT`), review the remote, then push:

```bash
git remote add origin https://github.com/YOUR_ACCOUNT/DevSkill-Hub.git
git remote -v
git push -u origin main
```

If Git is already initialized or a remote already exists, inspect and reuse it instead of reinitializing or replacing history. Add a repository star badge only after the actual owner/repository URL exists; no placeholder star badge is shipped.

准备好后由维护者手动初始化、提交、创建空远程仓库并推送。已有仓库时沿用原历史与远程。`YOUR_ACCOUNT` 是发布步骤中需要替换的说明值，不是已经创建的账号或仓库。

## Enable daily update pull requests

In the repository's **Settings → Actions → General**, allow the configured actions and enable **Allow GitHub Actions to create and approve pull requests** if your organization permits it. This project creates PRs and does not approve or merge them. An organization policy can prevent PR creation even if the workflow YAML requests the required permissions.

The validation workflow has `contents: read`. The scheduled update job grants only `contents: write` and `pull-requests: write`, required to maintain its dedicated branch and PR. It does not push updates to the default branch. It reuses `automation/update-stars` rather than opening a new branch for every snapshot. The schedule is 03:17 UTC daily (11:17 in China); GitHub may delay scheduled runs.

After publication, use **Actions → Update repository stars → Run workflow** for the first run. Inspect the diff and merge the PR manually. Successful refreshes update the observation timestamp even if counts are unchanged, so daily snapshots can produce timestamp-only diffs.

The separate **Check upstream changes** workflow runs weekly on Mondays at 03:43 UTC (11:43 in China). It compares skill directories, README/plugin metadata, and license paths with the recorded YAML baselines, proposing `docs/upstream-status.md` changes on `automation/upstream-review`. It does not update review claims or merge its PR. An unchanged report produces no new PR. See the [current upstream report](upstream-status.md).

GitHub's current documentation says that `pull_request` events for opened, synchronized, or reopened PRs created with `GITHUB_TOKEN` can create workflow runs in an **approval-required** state. A user with write access can select **Approve workflows to run** on the PR. Push events created with that token do not trigger a fresh workflow. The update job also runs validation, rendering checks, link checks, and tests **before** creating the PR. If branch protection requires a separate status check, approve the pending run, run validation manually on the automation branch, or use a suitable GitHub App token under your policy.

每天的自动化仅提出 PR，不自动批准或合并。仓库和组织需要允许 Actions 创建 PR。按 GitHub 当前文档，默认 Token 创建或更新的 PR 可产生需要人工批准的工作流；有写权限的维护者可点击 Approve workflows to run。更新任务本身也在提交前执行检查。分支保护需要独立状态检查时，可批准待运行工作流、对自动化分支手动运行验证，或按组织政策配置 App Token。

See the official [create-pull-request permissions documentation](https://github.com/peter-evans/create-pull-request#workflow-permissions) and [GitHub workflow trigger documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow). GitHub's trigger documentation governs this behavior where an action README gives older guidance.

## Optional release

After review and publication, a maintainer can tag `v0.1.0` and draft a GitHub release describing this registry's scope and verification limits. A release is not required to browse or maintain the directory, and none has been published automatically.
