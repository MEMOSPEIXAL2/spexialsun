# 云端维护与零基础指南

核对日期：2026-11-26。当前依据是 [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)，而非旧版 [Codex Cloud Legacy](https://learn.chatgpt.com/docs/environments/cloud-environment)。

## 当前环境与初始化

本次从 Default 类型的无仓库工作区开始，手工克隆到 `/workspace/spexialsun`。平台根目录的 `.git`、`.agents`、`.codex` 为只读占位，不能在那里初始化。仓库子目录可写。不要修改平台代理、凭据注入或只读全局配置。

基础入口：从仓库运行 `bash scripts/bootstrap.sh`。它可重复执行、不访问网络、不下载依赖、不改全局配置；输出在被忽略的 artifacts/ 中。要保存受版本控制的测试证据，按测试 Skill 的步骤写入 docs/reports。没有外部依赖，所以未添加空的包清单。

在当前云端机制中，可复用配置有 Install script 和 Start skill，需在平台保存并发布才对新任务可用。可将基础检查入口作为该环境的 Install script 最后一步；当前没有服务要启动，不需要为了形式创建 Start skill。把脚本放进仓库并不会自动注册平台设置。旧版环境的 setup/maintenance、缓存时间和 secrets 生命周期不可直接套用于当前环境。

项目规则：[AGENTS.md 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。全局与项目级指令分层，项目内越接近工作目录的规则越具体，AGENTS.override.md 优先于同层 AGENTS.md。应从目标仓库目录启动；不要指望在 `/workspace` 启动的既有会话自动加载新建子目录的规则。本次创建后已由执行者读取并遵守。

## 新建可复用环境（需要账户界面操作）

本次未调用平台发布操作；source_config_id 为 null，不能声称已经有模板。

1. 桌面应用打开 **Settings → Codex Cloud → Environments → Create environment**。也可在新任务选择 **Work in → Cloud → Select environment → Create environment**。
2. 选择 **MEMOSPEIXAL2/spexialsun**。初始成果仅在 **codex/cloud-foundation-20261126** 分支；若分支可选，选择它。尚无 main 时不要选一个不存在的 main。
3. 点击 **Get started**，在设置会话要求检查当前仓库并运行 `bash scripts/bootstrap.sh`。确认安装步骤没有失败，且实际工作目录是本仓库。
4. 核对权限与网络。当前任务网络为 unrestricted，未擅自收紧以免影响后续工作；有明确依赖后可关闭 **Enable all public internet access**，开启 **Package managers** 并补充实际需要的域名。不要禁用 HTTPS 验证。
5. 审查设置与文件，按界面提供的 **Save draft** 保存，然后点击 **Publish**。若界面是运行中聊天的 **Environment → Edit**，可先 **Apply to this chat**，再 **Save for future chats → 命名 → Save environment**；以实际界面为准。
6. 看到 **Environment published** 后点 **Start a new task**。确认分支后让 Codex“执行云端基础冒烟检查，说明发现和使用了哪个 Skill”，再显式选择 cloud-smoke 测试。检查报告写入并提交。只有这一步完成才能确认新任务宿主识别与环境复用。

当前执行端没有环境发布工具；创建新聊天只应由用户明确请求或从界面进行，不能用本机新进程冒充新云端任务。后续修改模板需 **Edit → 保存 → Republish**，新任务使用新版本，其他现有任务保持自身状态。

## 保存、合并与回滚（零基础）

Git 提交是一个版本，分支是一条独立修改线，推送是把版本保存到 GitHub，Pull Request（PR）是请求把分支改动合并到另一条分支。[GitHub PR 说明](https://docs.github.com/en/pull-requests/reference/pull-requests)。

空仓库没有真实的 main 提交，无法正常创建以 main 为基线的 PR。本次不为了 PR 人为写入 main 或重写历史；成果先推送独立分支。首次推送可能使该分支成为 GitHub 默认分支，以报告中的远端实测为准。

- 查看文件：打开 [仓库 Code 页面](https://github.com/MEMOSPEIXAL2/spexialsun)，点击左上分支下拉框，选择 **codex/cloud-foundation-20261126**；确认能看到 README.md、AGENTS.md、docs 和 scripts。点提交记录查看保存历史。
- 第一次采用成果：空仓库没有需要合并的旧成果，可以直接以该成果分支开始。若希望默认分支统一叫 main，可让 Codex在审查通过后从已验收提交创建 main，并再设置默认分支；本次不擅自执行这项默认分支变更。
- 以后修改：在新分支提交后打开 **Pull requests → New pull request**；base 选择实际存在的默认分支，compare 选择修改分支；点 **Create pull request**，检查 **Files changed** 与 **Checks**，验收后点 **Merge pull request → Confirm merge**（有权限且检查通过时）。
- 回滚：不要删除历史。请 Codex针对具体有问题的提交创建 revert 提交和分支，测试后提交 PR。若使用 GitHub 已合并 PR 页的 **Revert** 按钮，随后仍需审查并合并恢复 PR。

日常可说：“读取 docs/context.md，检查远端与当前分支，在新分支继续工作，验证后提交并推送”。不要仅说“记住这个信息”而不保存到文件。

## 本地与云端同步

本地克隆同一个仓库和分支，安装本地 Codex 后从仓库目录启动；仓库 Skill 随 git pull 获取，个人 Skill 与平台插件需分别管理。切换设备前提交并推送；另一端先检查未提交修改，再 fetch、比较并 pull --ff-only；有分叉时让 Codex处理，不强推。

每个新云端任务有独立工作区；未提交文件、虚拟环境和当前会话上下文不自动同步。当前官方说明默认任务 VM 状态恢复窗口为最后活动后最多七天，不能把它作为长期备份。GitHub 保存文本和代码版本；大型数据/模型/图纸按实际需要使用 Git LFS 或独立资料库，并在项目记录版本、校验值和访问方式。

## 排障

- **Skill 文件存在但没显示**：检查 CWD、分支、.agents/skills 路径、front matter、同名项和启用策略；刷新/重启。运行 check 通过只证明项目校验，不证明宿主发现。
- **本次 CLI app-server 失败**：默认只读 Codex home 无法初始化 SQLite；临时数据库/日志配置仍报只读错误。不要复制凭据或放宽全局沙箱；使用宿主支持的选择器，或在允许写入用户状态目录的独立本地安装中复测。
- **依赖下载失败**：分别检查域名、包管理器和凭据范围；不打印环境变量值。保持继承代理与 CA 设置。
- **Git push 失败**：先检查错误与账户对该仓库的 push 权限，按连接器提示修复授权后再重试，不把令牌写进 remote URL。
- **check 失败**：看 Git diff，辨别合法修改与意外变化；复核后才登记。完整性校验不是全面恶意代码检测。
- **找不到旧文件**：先确认是同一云端聊天、仓库和分支，再检查 GitHub 提交；新任务不等于原任务恢复。
