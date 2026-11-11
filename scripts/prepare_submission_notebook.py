"""Package the current notebook and embedded helpers into a standalone copy.

Preserves current implementation and policy instead of replaying historical
patches. Equivalent source keeps saved outputs; changed helper/pin behavior
clears them. Never commits, pushes, overwrites the source or fabricates ratings.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
HELPERS = {'SUBMISSION_SUPPORT_SOURCE': 'submission_support.py',
           'MCP_SERVER_SOURCE': 'mcp_indicator_server.py',
           'DEFENCE_SOURCE': 'defence_hardening.py'}


def assignments(source):
    cleaned = '\n'.join('pass' if line.lstrip().startswith('%') else line
                        for line in source.splitlines())
    return {node.targets[0].id: node for node in ast.parse(cleaned).body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)}


def replace_assignment(source, node, value):
    lines = source.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1]) + value + '\n' + ''.join(lines[node.end_lineno:])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT/'Phishing_Email_Triage.ipynb')
    parser.add_argument('--output', type=Path, default=ROOT/'output/submission/P13_Phishing_Email_Triage.ipynb')
    parser.add_argument('--asset-revision', help='Immutable local Git commit containing the published runtime assets.')
    parser.add_argument('--ratings', type=Path, action='append', default=[],
                        help='Additional rated snapshot under artifacts; requires --asset-revision.')
    parser.add_argument('--clear-outputs', action='store_true', help='Prepare an explicitly unexecuted copy.')
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error('Use a separate output file; the canonical source is preserved.')
    if args.ratings and not args.asset_revision:
        parser.error('--ratings requires the immutable --asset-revision containing those entries.')
    notebook = json.loads(args.source.read_text(encoding='utf-8'))
    revision = None
    if args.asset_revision:
        revision = subprocess.check_output(['git', 'rev-parse', args.asset_revision+'^{commit}'],
                                           cwd=ROOT, text=True).strip()
    embedded = set()
    behavior_changed = False
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell['source'])
        nodes = assignments(source)
        changes = []
        for variable, filename in HELPERS.items():
            if variable in nodes:
                text = (ROOT/filename).read_text(encoding='utf-8')
                changes.append((nodes[variable], variable+' = '+repr(text)))
                embedded.add(filename)
        if 'PINNED_REQUIREMENTS' in nodes:
            changes.append((nodes['PINNED_REQUIREMENTS'],
                            'PINNED_REQUIREMENTS = '+repr((ROOT/'requirements.txt').read_text(encoding='utf-8'))))
        if revision and 'SAVED_ASSET_MANIFEST' in nodes:
            manifest = ast.literal_eval(nodes['SAVED_ASSET_MANIFEST'].value)
            for path in args.ratings:
                relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
                if not relative.startswith('artifacts/') or path.suffix != '.csv':
                    raise ValueError('Additional rating snapshots must be CSVs under artifacts/.')
                manifest[relative] = ''
            manifest = {name: hashlib.sha256(subprocess.check_output(
                ['git', 'show', revision+':'+name], cwd=ROOT)).hexdigest() for name in manifest}
            changes.extend([(nodes['ASSET_REVISION'], 'ASSET_REVISION = '+repr(revision)),
                            (nodes['SAVED_ASSET_MANIFEST'], 'SAVED_ASSET_MANIFEST = '+repr(manifest))])
        for node, value in sorted(changes, key=lambda item: item[0].lineno, reverse=True):
            source = replace_assignment(source, node, value)
        behavior_changed |= ast.dump(ast.parse('\n'.join(
            'pass' if line.lstrip().startswith('%') else line for line in ''.join(cell['source']).splitlines()))) != ast.dump(
                ast.parse('\n'.join('pass' if line.lstrip().startswith('%') else line for line in source.splitlines())))
        cell['source'] = source.splitlines(keepends=True)
    if embedded != set(HELPERS.values()):
        raise ValueError('The notebook is missing an expected embedded helper.')
    clear_outputs = args.clear_outputs or behavior_changed
    if clear_outputs:
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                cell['execution_count'], cell['outputs'] = None, []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(notebook, indent=1, ensure_ascii=False)+'\n'
    args.output.write_text(payload, encoding='utf-8', newline='\n')
    provenance = {'source': str(args.source.resolve()),
        'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
        'packaged_sha256': hashlib.sha256(payload.encode()).hexdigest(),
        'source_cells_sha256': hashlib.sha256(json.dumps(
            [''.join(c['source']) for c in notebook['cells']]).encode()).hexdigest(),
        'embedded_helpers': sorted(embedded), 'outputs_cleared': clear_outputs,
        'packaging_changed_code_behavior': behavior_changed,
        'asset_revision_updated': revision}
    args.output.with_suffix('.provenance.json').write_text(json.dumps(provenance, indent=2)+'\n',
                                                        encoding='utf-8', newline='\n')
    print(args.output)


if __name__ == '__main__':
    main()
