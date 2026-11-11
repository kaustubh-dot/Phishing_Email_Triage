"""Check preserved notebook outputs, model-code lineage and human-review evidence.

This verifies a supplied executed artifact. It does not claim a new model run.
"""
import argparse
import ast
import csv
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class DataFrameTable(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        elif tag in {'td', 'th'} and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in {'td', 'th'} and self.cell is not None:
            self.row.append(''.join(self.cell).strip())
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None

    def records(self):
        header, *rows = self.rows
        if header[0] == '':
            header, rows = header[1:], [row[1:] for row in rows]
        return [dict(zip(header, row)) for row in rows]


def table_records(cell, position=0):
    tables = [output['data']['text/html'] for output in cell.get('outputs', [])
              if 'text/html' in output.get('data', {})]
    parser = DataFrameTable()
    value = tables[position]
    parser.feed(''.join(value) if isinstance(value, list) else value)
    return parser.records()


def verify(notebook_path, supplied_path=None):
    import nbformat
    import pandas as pd
    from submission_support import load_human_reviews

    notebook = nbformat.read(notebook_path, as_version=4)
    nbformat.validate(notebook)
    code = [cell for cell in notebook.cells if cell.cell_type == 'code']
    assert len(code) == 21 and all(cell.execution_count is not None for cell in code)
    assert not any(output.output_type == 'error' for cell in code for output in cell.outputs)
    lineage = notebook.metadata['p13_saved_execution']
    if supplied_path:
        assert hashlib.sha256(supplied_path.read_bytes()).hexdigest() == lineage['source_notebook_sha256']
    for index, expected in lineage['model_cell_ast_sha256'].items():
        module = ast.parse(notebook.cells[int(index)].source)
        if index == '20':
            module.body = [node for node in module.body if not (
                isinstance(node, ast.FunctionDef) and node.name == 'explanation_quality_warnings')]
        actual = hashlib.sha256(ast.dump(module, include_attributes=False).encode()).hexdigest()
        assert actual == expected, f'Model logic changed in cell {index}; retain new execution evidence.'
    with (ROOT/'artifacts/results/full/classification_metrics.csv').open(encoding='utf-8', newline='') as stream:
        metrics = {row['condition']: row for row in csv.DictReader(stream)}
    displayed = table_records(notebook.cells[24])
    assert len(displayed) == len(metrics) == 10
    for row in displayed:
        original = metrics[row['condition']]
        for name in ['n', 'accuracy', 'precision', 'recall', 'f1', 'false_positive_rate']:
            assert round(float(original[name]), 4) == float(row[name]), (row['condition'], name)
    confirmation = json.loads((ROOT/'artifacts/human_review_confirmation.json').read_text(encoding='utf-8'))
    cases = pd.read_csv(ROOT/'artifacts/human_explanation_ratings_9b10d09848942b57.csv')
    reviews = load_human_reviews(cases, ROOT/confirmation['review_entries'], confirmation)
    assert reviews['completed'] == 30 and reviews['snapshot_matches']
    summary = json.loads((ROOT/'artifacts/results/full/run_summary.json').read_text(encoding='utf-8'))
    components = json.loads((ROOT/'artifacts/results/full/component_metrics.json').read_text(encoding='utf-8'))
    assert summary['human_reviews_completed'] == components['human_reviews_completed'] == 30
    assert summary['human_ratings_completed'] == components['human_ratings_completed'] == 30
    assert summary['human_rater_counts'] == reviews['rater_counts']
    summary_output = next(output.data['text/plain'] for output in notebook.cells[37].outputs
                          if 'text/plain' in output.get('data', {}))
    saved_summary = ast.literal_eval(summary_output)
    assert saved_summary['human_reviews_completed'] == 30
    assert saved_summary['runtime_seconds'] == summary['runtime_seconds'] == 194.9
    for value in [saved_summary, summary, components]:
        assert value['human_review_snapshot_verified']
    spec = importlib.util.spec_from_file_location('metrics_verifier', ROOT/'scripts/verify_submission_results.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    metrics_check = module.verify(ROOT/'artifacts/results/full')
    return {'status': 'pass',
        'notebook_sha256': hashlib.sha256(notebook_path.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
        'notebook_hash_convention': 'Canonical UTF-8 LF Git blob',
        'source_cells_sha256': hashlib.sha256(json.dumps([cell.source for cell in notebook.cells]).encode()).hexdigest(),
        'supplied_execution_code_cells': 21, 'saved_error_outputs': 0,
        'model_code_matches_supplied_execution': True, 'saved_classification_rows_checked': 10,
        'human_based_reviews_completed': 30, 'human_review_snapshot_verified': True,
        'fresh_model_execution_performed': False, 'numeric_results': metrics_check}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notebook', type=Path, default=ROOT/'Phishing_Email_Triage.ipynb')
    parser.add_argument('--supplied', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = verify(args.notebook, args.supplied)
    text = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8', newline='\n')
    print(text)


if __name__ == '__main__':
    main()
