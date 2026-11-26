"""Project inventory and integrity checks; deliberately supports simple front matter only."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / '.agents/skills'
LOCK = ROOT / 'skills-lock.json'


def inventory():
    result = {}
    names = set()
    for directory in sorted(SKILLS.iterdir()):
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError(f'only real skill directories allowed: {directory.name}')
        content = (directory / 'SKILL.md').read_text()
        parts = content.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f'missing front matter: {directory.name}')
        fields = {}
        for line in parts[1].splitlines():
            if line.strip():
                key, value = line.split(':', 1)
                fields[key.strip()] = value.strip()
        name = fields.get('name', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
            raise ValueError(f'invalid skill name: {directory.name}')
        if name != directory.name or name in names or not fields.get('description'):
            raise ValueError(f'name/description conflict: {directory.name}')
        names.add(name)
        hashes = {}
        for path in sorted(directory.rglob('*')):
            if path.is_symlink():
                raise ValueError(f'symlink requires manual review: {path.relative_to(ROOT)}')
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                hashes[str(path.relative_to(directory))] = hashlib.sha256(path.read_bytes()).hexdigest()
        result[name] = hashes
    if not result:
        raise ValueError('no project skills found')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'record'])
    parser.add_argument('--name')
    parser.add_argument('--source')
    parser.add_argument('--revision')
    parser.add_argument('--license')
    parser.add_argument('--review', help='public-safe summary of actual manual review')
    args = parser.parse_args()
    try:
        current = inventory()
        lock = json.loads(LOCK.read_text()) if LOCK.exists() else {'schema_version': 1, 'skills': {}}
        if lock.get('schema_version') != 1:
            raise ValueError('unsupported lock schema')
        if args.command == 'record':
            if not all([args.name, args.source, args.revision, args.license, args.review]):
                parser.error('record requires --name --source --revision --license --review')
            if args.name not in current:
                raise ValueError('skill not found')
            lock['skills'][args.name] = {
                'source': args.source, 'revision': args.revision, 'license': args.license,
                'review': args.review, 'files': current[args.name]}
            LOCK.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + '\n')
            print('Recorded reviewed files:', args.name)
        else:
            recorded = {name: entry['files'] for name, entry in lock['skills'].items()}
            if current != recorded:
                raise ValueError('inventory/hash mismatch; review changes before recording or remove stale entry after uninstall')
            print(f'PASS: {len(current)} skill(s); names, metadata and all file hashes match')
    except (OSError, ValueError, KeyError) as exc:
        print('FAIL:', exc)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
