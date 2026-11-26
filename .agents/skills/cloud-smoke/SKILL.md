---
name: cloud-smoke
description: 验证当前仓库云端基础环境并写入冒烟测试报告；当用户要求“云端基础冒烟检查”或“云端基础环境自检”时使用。不要用于完整安全审计、网络修复或第三方 Skill 安装。
---

# 云端基础冒烟检查

1. 确认当前工作目录为包含本文件的 Git 仓库根目录，读取 `AGENTS.md`。
2. 执行 `python3 scripts/skills.py check`；失败时停止并报告，不修改校验清单绕过错误。
3. 执行 `python3 .agents/skills/cloud-smoke/scripts/smoke.py --output docs/reports/smoke-latest.json`。
4. 读取生成的 JSON，确认 `status` 是 `passed`，并报告检查数量与输出路径。
5. 明确这仅证明文件检查与流程执行；不能据此声称宿主自动发现、自动调用或新云端任务验证通过。

脚本只使用 Python 标准库，不访问网络、不读取环境变量、不输出凭据、不创建提交。
