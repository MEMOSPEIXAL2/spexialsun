"""Negative checks for the inventory guard, using disposable repository copies."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class InventoryGuard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['scripts', '.agents']:
            shutil.copytree(ROOT / name, self.root / name, ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copyfile(ROOT / 'skills-lock.json', self.root / 'skills-lock.json')

    def check_code(self):
        return subprocess.run(['python3', str(self.root / 'scripts/skills.py'), 'check'],
                              capture_output=True, text=True).returncode

    def test_unchanged_passes(self):
        self.assertEqual(self.check_code(), 0)

    def test_modified_script_rejected(self):
        path = self.root / '.agents/skills/cloud-smoke/scripts/smoke.py'
        path.write_text(path.read_text() + '\n# unintended change\n')
        self.assertNotEqual(self.check_code(), 0)

    def test_untracked_skill_file_rejected(self):
        (self.root / '.agents/skills/cloud-smoke/unreviewed.txt').write_text('new file')
        self.assertNotEqual(self.check_code(), 0)

    def test_link_rejected(self):
        (self.root / '.agents/skills/cloud-smoke/link').symlink_to('/etc/hosts')
        self.assertNotEqual(self.check_code(), 0)

    def test_name_mismatch_rejected(self):
        path = self.root / '.agents/skills/cloud-smoke/SKILL.md'
        path.write_text(path.read_text().replace('name: cloud-smoke', 'name: wrong-name'))
        self.assertNotEqual(self.check_code(), 0)


if __name__ == '__main__':
    unittest.main()
