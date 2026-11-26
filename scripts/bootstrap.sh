#!/usr/bin/env bash
# Repeatable offline validation; no automatic downloads or global configuration edits.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
command -v git >/dev/null
command -v python3 >/dev/null
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python >=3.10 required"'
git rev-parse --show-toplevel
python3 scripts/skills.py check
python3 .agents/skills/cloud-smoke/scripts/smoke.py --output artifacts/bootstrap-smoke.json
printf '%s\n' '基础验证完成；此脚本不会注册环境配置或证明宿主调用成功。'
