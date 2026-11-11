"""Ensure repackaging does not discard a submission's valid saved outputs."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackagedOutputTests(unittest.TestCase):
    def package(self, directory, *flags):
        output = Path(directory)/'submission.ipynb'
        subprocess.run([sys.executable, str(ROOT/'scripts/prepare_submission_notebook.py'),
            '--output', str(output), *flags], cwd=ROOT, check=True, capture_output=True, text=True)
        return json.loads(output.read_text(encoding='utf-8'))

    def test_equivalent_repackaging_preserves_all_saved_results(self):
        source = json.loads((ROOT/'Phishing_Email_Triage.ipynb').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as directory:
            packaged = self.package(directory)
        for before, after in zip(source['cells'], packaged['cells']):
            if before['cell_type'] == 'code':
                self.assertEqual(before['execution_count'], after['execution_count'])
                self.assertEqual(before['outputs'], after['outputs'])

    def test_explicit_fresh_copy_clears_results(self):
        with tempfile.TemporaryDirectory() as directory:
            packaged = self.package(directory, '--clear-outputs')
        for cell in packaged['cells']:
            if cell['cell_type'] == 'code':
                self.assertIsNone(cell['execution_count'])
                self.assertEqual(cell['outputs'], [])
