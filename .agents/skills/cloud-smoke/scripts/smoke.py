"""Offline smoke workflow; no third-party packages or secrets."""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='docs/reports/smoke-latest.json')
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if ROOT not in output.parents or output.is_symlink():
        parser.error('output must be a file inside this repository')
    checks = {name: (ROOT / name).is_file() for name in [
        'AGENTS.md', 'README.md', 'skills-lock.json',
        '.agents/skills/cloud-smoke/SKILL.md', 'docs/context.md']}
    probe = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--show-toplevel'],
                           text=True, capture_output=True, check=False)
    checks['git_root'] = probe.returncode == 0 and Path(probe.stdout.strip()).resolve() == ROOT
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {'schema_version': 1, 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
              'status': 'passed' if all(checks.values()) else 'failed', 'checks': checks,
              'scope': 'offline workflow only; host invocation and cross-task persistence not implied'}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
