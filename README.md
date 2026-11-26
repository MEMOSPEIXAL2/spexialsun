# spexialsun

建筑设计、科学研究与程序开发的长期工作基础仓库。当前仅提供环境验证、项目 Skill 和持久上下文约定；尚无业务项目或第三方依赖。

## 开始使用

```bash
git clone https://github.com/MEMOSPEIXAL2/spexialsun.git
cd spexialsun
# 首次成果位于 codex/cloud-foundation-20261126；远端尚无 main 基线
# 如当前检出分支不同：git switch codex/cloud-foundation-20261126
bash scripts/bootstrap.sh
```

最低要求：Git、Bash、Python 3.10+。Node.js 按未来项目需要使用，目前无需 npm install 或 pip install。

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
