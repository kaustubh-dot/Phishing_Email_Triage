"""Exercise MCP inside a real notebook kernel, including Windows loop handling."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]


class NotebookMCPTests(unittest.TestCase):
    def test_actual_notebook_mcp_cell(self):
        notebook = json.loads((ROOT/'Phishing_Email_Triage.ipynb').read_text(encoding='utf-8'))
        source = next(''.join(cell['source']) for cell in notebook['cells']
                      if 'async def verify_mcp_server()' in ''.join(cell['source']))
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            spec = work/'kernels/p13-mcp-test'
            spec.mkdir(parents=True)
            (spec/'kernel.json').write_text(json.dumps({
                'argv': [sys.executable, '-X', 'utf8', '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
                'display_name': 'P13 MCP test', 'language': 'python'}), encoding='utf-8')
            setup = (f'import sys, json\nfrom pathlib import Path\nsys.path.insert(0, {str(ROOT)!r})\n'
                'import mcp_indicator_server\nindicator_namespace = vars(mcp_indicator_server)\n'
                f'mcp_server_path = Path({str(ROOT / "mcp_indicator_server.py")!r})\n'
                f'RUN = Path({str(work)!r})\n'
                'def save_json(path, value):\n'
                '    path.write_text(json.dumps(value), encoding="utf-8")\n')
            nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(setup+source)])
            manager = KernelManager(kernel_name='p13-mcp-test',
                kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(work/'kernels')]))
            client = NotebookClient(nb, km=manager, timeout=60,
                resources={'metadata': {'path': str(work)}})
            try:
                client.execute()
            finally:
                try:
                    if manager.has_kernel:
                        manager.shutdown_kernel(now=True)
                finally:
                    if client.kc is not None:
                        client.kc.stop_channels()
            result = json.loads((work/'mcp_checks.json').read_text(encoding='utf-8'))
            self.assertEqual(result['parity_cases_passed'], 3)
            self.assertTrue(result['invalid_arguments_rejected'])
            self.assertFalse(result['quarantine_tool_exposed'])


if __name__ == '__main__':
    unittest.main()
