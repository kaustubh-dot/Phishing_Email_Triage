"""Execute a submission notebook in a temporary workspace, with explicit evidence.

AI-assisted. Only Hugging Face model/dataset caches are shared. A cold-assets run
starts with none of the repository artifacts; --reuse-assets also checks offline
reruns while preserving locally completed ratings. Never commits or pushes.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notebook',type=Path,default=ROOT/'Phishing_Email_Triage.ipynb')
    parser.add_argument('--mode',choices=['full','quick'],default='full')
    parser.add_argument('--reuse-assets',type=Path)
    parser.add_argument('--save-executed',action='store_true')
    args=parser.parse_args()
    if not (ROOT/'.cache/huggingface').is_dir():
        parser.error('Run the notebook first to populate the project Hugging Face caches; this optional verifier reuses them offline.')
    import nbformat
    from nbclient import NotebookClient
    from jupyter_client import KernelManager
    from jupyter_client.kernelspec import KernelSpecManager
    check=Path(tempfile.mkdtemp(prefix=f'p13-reviewed-{args.mode}-'))
    work=check/'notebook-only'
    work.mkdir()
    runtime=work/'p13_runtime'
    runtime.mkdir()
    (runtime/'.cache').symlink_to(ROOT/'.cache',target_is_directory=True)
    if args.reuse_assets:
        shutil.copytree(args.reuse_assets/'artifacts',runtime/'artifacts')
    kernels=check/'kernels'
    spec=kernels/'p13-reviewed'
    spec.mkdir(parents=True)
    (spec/'kernel.json').write_text(json.dumps({'argv':[
        str(ROOT/'.venv/bin/python'),'-m','ipykernel_launcher','-f','{connection_file}'],
        'display_name':'P13 reviewed notebook verification','language':'python'}))
    os.environ.update(P13_QUICK_RUN='1' if args.mode=='quick' else '0',
        HF_HUB_OFFLINE='1',HF_DATASETS_OFFLINE='1',PIP_DISABLE_PIP_VERSION_CHECK='1',
        IPYTHONDIR=str(check/'ipython'),JUPYTER_RUNTIME_DIR=str(check/'jupyter-runtime'))
    os.environ.pop('P13_WORKSPACE',None)
    notebook=nbformat.read(args.notebook,as_version=4)
    nbformat.validate(notebook)
    source_hash=hashlib.sha256(json.dumps([cell.source for cell in notebook.cells]).encode()).hexdigest()
    shutil.copy2(args.notebook,work/args.notebook.name)
    manager=KernelManager(kernel_name='p13-reviewed',kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernels)]))
    def progress(cell,cell_index,**kwargs):
        if cell.cell_type=='code': print(f'Executing {args.mode} cell {cell_index}: {cell.source.splitlines()[0][:95]}',flush=True)
    client=NotebookClient(notebook,km=manager,timeout=1800,
        resources={'metadata':{'path':str(work)}},on_cell_start=progress)
    print(f'CHECK_DIRECTORY={check}',flush=True)
    started=time.monotonic()
    try:
        client.execute()
    except Exception:
        nbformat.write(notebook,check/'failed.ipynb')
        raise
    finally:
        manager.shutdown_kernel(now=True)
    wall_seconds=time.monotonic()-started
    code=[cell for cell in notebook.cells if cell.cell_type=='code']
    assert all(cell.execution_count is not None for cell in code)
    assert not any(o.output_type=='error' for c in code for o in c.outputs)
    nbformat.validate(notebook)
    if args.save_executed: nbformat.write(notebook,args.notebook)
    else: nbformat.write(notebook,check/'executed.ipynb')
    result=runtime/'artifacts/results'/args.mode
    summary=json.loads((result/'run_summary.json').read_text())
    assert summary['evaluated_test_size']==(300 if args.mode=='full' else 60)
    assert summary['human_rating_snapshot_verified']
    assert summary['human_ratings_completed']==0, 'Unexpected human scores in the frozen evaluation assets.'
    assert all(summary['approval_checks'].values())
    assert summary['quarantine_log_empty_at_end']
    evidence=ROOT/'output/submission/verification'/args.mode
    evidence.mkdir(parents=True,exist_ok=True)
    for filename in ['run_summary.json','environment.json','component_metrics.json',
        'classification_metrics.csv','predictions.csv','injection_metrics.csv','injection_common_metrics.csv',
        'security_holdout_metrics.csv','approval_checks.json','mcp_checks.json','classifier_input_overlap.json']:
        shutil.copy2(result/filename,evidence/filename)
    expected=ROOT/'artifacts/results'/args.mode
    if not (expected/'predictions.csv').exists() and args.mode=='quick':
        expected=ROOT/'archive/quick-run-2026-11-05'
    predictions_match=(expected/'predictions.csv').read_bytes()==(result/'predictions.csv').read_bytes()
    report={'mode':args.mode,'source_cells_sha256':source_hash,'executed_code_cells':len(code),
        'error_outputs':0,'wall_seconds_including_setup':round(wall_seconds,2),
        'cold_repository_assets':not bool(args.reuse_assets),'shared_huggingface_cache':True,
        'saved_predictions_match':predictions_match,'summary':summary}
    (evidence/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('VERIFICATION='+json.dumps(report),flush=True)
    print(f'RUNTIME_DIRECTORY={runtime}',flush=True)


if __name__=='__main__': main()
