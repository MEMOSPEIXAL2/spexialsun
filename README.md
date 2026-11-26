# spexialsun

建筑设计、科学研究与程序开发的长期工作基础仓库。提供环境验证、项目 Skill、持久上下文，以及已安装的文献综述技能与竹木低碳建筑材料试验。

文献综述入口：[使用指南](docs/literature-review-guide.md)、[选型与安装报告](docs/reports/literature-review-install/report.zh-CN.md)、[15篇文献真实试验](projects/renewable-materials-review/review.md)。科研依赖隔离安装，见 requirements-literature.lock；基础bootstrap仍离线且不依赖这些包。

## 开始使用

```bash
git clone https://github.com/MEMOSPEIXAL2/spexialsun.git
cd spexialsun
# 首次成果及当前默认分支为 codex/cloud-foundation-20261126；远端尚无 main 基线
# 如当前检出分支不同：git switch codex/cloud-foundation-20261126
bash scripts/bootstrap.sh
```

基础检查最低要求：Git、Bash、Python 3.10+。仅做基础检查无需安装依赖；文献DOI核验按使用指南建立.venv并同步锁定包，勿全局安装。

共享 Skill 位于 `.agents/skills`，从本仓库目录启动 Codex。桌面 Skill 选择器、CLI 的 `/skills` 或 `$cloud-smoke` 需要宿主实际发现后才能使用。云端未显示时先切换到本仓库，再重启/新建会话并检查，不要将读取文件等同于宿主发现。

## 结构与维护入口

- `AGENTS.md`：项目规则。
- `.agents/skills/cloud-smoke/`：离线测试 Skill。
- `scripts/bootstrap.sh`、`scripts/skills.py`：基础验证与 Skill 完整性登记。
- `skills-lock.json`：项目自有的来源、版本、审查与哈希清单，不是 Codex 内置配置。
- `docs/skills.md`：安装、审查、依赖、更新、卸载与恢复。
- `docs/maintenance.md`：云端初始化、同步、排障与零基础操作指南。
- `docs/context.md`：跨会话接续信息与决策记录。
- `docs/reports/`：脱敏检查报告及可复核结果。

目前仓库公开。密钥放平台 Personal vault / HTTP secrets；保密图纸、未公开论文、受版权限制的全文放合适的私有资料库，本仓库只记录获准公开的索引。

重要成果提交并推送到 GitHub。新云端任务有独立工作区，本地个人 Skill 不会自动同步；用 Git 同步项目 Skill。可复用的已安装软件环境需另外创建并 Publish，详见维护指南。
