"""Verify the final notebook in an isolated workspace on Windows or Linux.

Uses the active Python environment and shares cached models/data without
symlinks. Reports actual hardware, rating completion and prediction differences.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def prediction_comparison(reference, actual):
    """Compare CSV values independently of newlines and row order."""
    def load(path):
        with Path(path).open(encoding='utf-8', newline='') as stream:
            return {row['email_id']: row for row in csv.DictReader(stream)}
    if not Path(reference).exists():
        return {'reference_available': False, 'matches': None}
    old, new = load(reference), load(actual)
    if set(old) != set(new):
        return {'reference_available': True, 'matches': False, 'email_id_sets_match': False}
    old_columns = set(next(iter(old.values()))) - {'email_id'}
    new_columns = set(next(iter(new.values()))) - {'email_id'}
    missing_columns, extra_columns = sorted(old_columns-new_columns), sorted(new_columns-old_columns)
    columns = sorted(old_columns & new_columns)
    differences = {column: sum(old[key].get(column) != new[key].get(column) for key in old)
                   for column in columns}
    return {'reference_available': True,
            'matches': not (any(differences.values()) or missing_columns or extra_columns),
            'email_id_sets_match': True, 'different_rows_by_column': differences,
            'missing_columns': missing_columns, 'extra_columns': extra_columns}


def validate_rating_summary(summary, components):
    """Accept pending or completed real ratings; reject inconsistent counts."""
    completed = summary['human_ratings_completed']
    if summary['human_ratings_required'] != 30 or not isinstance(completed, int) or not 0 <= completed <= 30:
        raise ValueError('Invalid current explanation-rating count.')
    if not summary['human_rating_snapshot_verified']:
        raise ValueError('Current explanation-rating snapshot was not verified.')
    if components['human_ratings_completed'] != completed:
        raise ValueError('Component and final rating counts disagree.')
    if sum(summary['human_rater_counts'].values()) != completed:
        raise ValueError('Rater counts do not match completed current ratings.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notebook', type=Path, default=ROOT/'Phishing_Email_Triage.ipynb')
    parser.add_argument('--mode', choices=['full', 'quick'], default='full')
    parser.add_argument('--device', choices=['auto', 'cpu', 'cuda'], default='auto')
    parser.add_argument('--cache-dir', type=Path, default=ROOT/'.cache/huggingface')
    parser.add_argument('--reuse-assets', type=Path)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--allow-downloads', action='store_true')
    parser.add_argument('--timeout', type=int, default=14400, help='Seconds allowed per code cell; CPU generation can be slow.')
    parser.add_argument('--save-executed', action='store_true')
    args = parser.parse_args()
    cache = args.cache_dir.resolve()
    if not cache.exists() and not args.allow_downloads:
        parser.error('Populate --cache-dir, or pass --allow-downloads for first use.')
    cache.mkdir(parents=True, exist_ok=True)
    import nbformat
    from nbclient import NotebookClient
    from jupyter_client import KernelManager
    from jupyter_client.kernelspec import KernelSpecManager

    check = Path(tempfile.mkdtemp(prefix=f'p13-{args.device}-{args.mode}-'))
    work = check/'notebook-only'
    runtime = work/'p13_runtime'
    runtime.mkdir(parents=True)
    if args.reuse_assets:
        shutil.copytree(args.reuse_assets.resolve()/'artifacts', runtime/'artifacts',
                        ignore=shutil.ignore_patterns('checkpoints', 'results'))
    spec = check/'kernels/p13-verification'
    spec.mkdir(parents=True)
    (spec/'kernel.json').write_text(json.dumps({
        'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        'display_name': 'P13 notebook verification', 'language': 'python',
    }), encoding='utf-8')
    os.environ.update(P13_QUICK_RUN='1' if args.mode == 'quick' else '0',
        P13_WORKSPACE=str(runtime), P13_HF_HOME=str(cache), P13_DEVICE=args.device,
        PIP_DISABLE_PIP_VERSION_CHECK='1', IPYTHONDIR=str(check/'ipython'),
        JUPYTER_RUNTIME_DIR=str(check/'jupyter-runtime'))
    os.environ['PYTHONUTF8'] = '1'
    for name in ['HF_HUB_OFFLINE', 'HF_DATASETS_OFFLINE']:
        os.environ[name] = '0' if args.allow_downloads else '1'
    notebook = nbformat.read(args.notebook, as_version=4)
    nbformat.validate(notebook)
    source_hash = hashlib.sha256(json.dumps([c.source for c in notebook.cells]).encode()).hexdigest()
    shutil.copy2(args.notebook, work/args.notebook.name)
    manager = KernelManager(kernel_name='p13-verification',
        kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(check/'kernels')]))
    started = time.monotonic()
    def progress(cell, cell_index, **kwargs):
        if cell.cell_type == 'code':
            print(f'[{time.monotonic()-started:.1f}s] Executing cell {cell_index}: '
                  f'{cell.source.splitlines()[0][:95]}', flush=True)
    client = NotebookClient(notebook, km=manager, timeout=args.timeout,
        resources={'metadata': {'path': str(work)}}, on_cell_start=progress)
    print(f'CHECK_DIRECTORY={check}', flush=True)
    try:
        client.execute()
    except Exception:
        nbformat.write(notebook, check/'failed.ipynb')
        print(f'Failed notebook preserved at {check / "failed.ipynb"}', flush=True)
        raise
    finally:
        try:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
        finally:
            if client.kc is not None:
                client.kc.stop_channels()
    wall_seconds = time.monotonic()-started
    code = [c for c in notebook.cells if c.cell_type == 'code']
    assert all(c.execution_count is not None for c in code)
    assert not any(o.output_type == 'error' for c in code for o in c.outputs)
    nbformat.validate(notebook)
    result = runtime/'artifacts/results'/args.mode
    summary = json.loads((result/'run_summary.json').read_text(encoding='utf-8'))
    components = json.loads((result/'component_metrics.json').read_text(encoding='utf-8'))
    environment = json.loads((result/'environment.json').read_text(encoding='utf-8'))
    assert summary['evaluated_test_size'] == (300 if args.mode == 'full' else 60)
    assert all(summary['approval_checks'].values())
    assert summary['quarantine_log_empty_at_end']
    if args.device != 'auto':
        assert summary['device'] == args.device
    validate_rating_summary(summary, components)
    evidence = (args.output_dir or ROOT/'output/submission/verification'/f'{args.device}-{args.mode}').resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    reference = ROOT/'artifacts/results'/args.mode/'predictions.csv'
    if args.mode == 'quick' and not reference.exists():
        reference = ROOT/'archive/quick-run-2026-11-05/predictions.csv'
    comparison = prediction_comparison(reference, result/'predictions.csv')
    for path in result.iterdir():
        if path.is_file():
            shutil.copy2(path, evidence/path.name)
    ratings = runtime/summary['human_rating_sheet']
    shutil.copy2(ratings, evidence/ratings.name)
    nbformat.write(notebook, evidence/'executed.ipynb')
    dependency_check = subprocess.run([sys.executable, '-m', 'pip', 'check'], capture_output=True, text=True)
    report = {'mode': args.mode, 'source_cells_sha256': source_hash,
        'executed_code_cells': len(code), 'error_outputs': 0,
        'wall_seconds_including_setup': round(wall_seconds, 2),
        'cell_timeout_seconds': args.timeout,
        'cold_repository_assets': not bool(args.reuse_assets),
        'shared_huggingface_cache': True, 'downloads_allowed': args.allow_downloads,
        'reused_embedding_cache': bool(args.reuse_assets and (args.reuse_assets/'artifacts/embeddings').exists()),
        'python_executable': sys.executable, 'python_version': sys.version,
        'device': environment['device'], 'gpu': environment.get('gpu'),
        'dependency_check': {'passed': dependency_check.returncode == 0, 'output': dependency_check.stdout.strip()},
        'prediction_comparison': comparison, 'saved_predictions_match': comparison['matches'],
        'summary': summary}
    (evidence/'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    if args.save_executed:
        nbformat.write(notebook, args.notebook)
    print('VERIFICATION='+json.dumps(report), flush=True)
    print(f'RUNTIME_DIRECTORY={runtime}', flush=True)


if __name__ == '__main__':
    main()
