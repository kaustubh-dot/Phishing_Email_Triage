"""Prepare the reviewed one-file submission locally; never commits or pushes.

AI-assisted. Reads the supplied notebook as data, preserves its system, and applies
explicit setup, rating-provenance, documentation and demo improvements.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'kaustubh-dot/Phishing_Email_Triage'
REVISION = '044821a93fc84c4b1165caea57ca8c7f63bfb414'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'output/submission/P13_Phishing_Email_Triage.ipynb')
    args = parser.parse_args()
    notebook = json.loads(args.source.read_text())
    assert len(notebook['cells']) == 38, 'Review a structural change before applying these patches.'
    cells = notebook['cells']
    sources = [''.join(cell['source']) for cell in cells]
    support = (ROOT/'submission_support.py').read_text()
    assets = ['artifacts/revisions.json']
    for rank in ['r4', 'r8', 'defended-r8']:
        assets.extend(f'artifacts/adapters/{rank}/{name}' for name in
                      ['adapter_config.json', 'adapter_model.safetensors', 'training_metadata.json'])
    assets.extend(str(p.relative_to(ROOT)) for p in sorted((ROOT/'artifacts').glob('human_explanation_ratings*.csv')))
    assets.extend(['artifacts/security/development_specs.json', 'artifacts/security/heldout_specs.json'])
    manifest = {name: sha256((ROOT/name).read_bytes()).hexdigest() for name in assets}
    pins = (ROOT/'requirements.txt').read_text()
    revisions = json.loads((ROOT/'artifacts/revisions.json').read_text())

    sources[0] = sources[0].replace('on this branch need team review', 'need team review')
    sources[0] += '\n\n**Project repository:** [kaustubh-dot/Phishing_Email_Triage](https://github.com/kaustubh-dot/Phishing_Email_Triage). For the presentation, supporting results, archived experiments and further implementation details, check the repository. The required system, evaluation, saved outputs and demo remain in this notebook. Saved runtime assets are fetched from the pinned snapshot identified in Setup.\n\n**Current validation status:** automated correctness and quote checks are separate from human explanation quality. Only ratings of the exact current explanations count. Full and quick executions have completed successfully on NVIDIA RTX 4000 Ada; these execution checks do not imply perfect classification or verified performance on another device. Team review remains required.\n'
    sources[2] = '''## 2. Setup

This notebook can start in an empty folder with Python 3.12 and internet access. It writes its pinned dependency list and support module, then fetches only missing saved adapters, revision records, frozen fixtures and rating sheets from a fixed public GitHub commit. Every downloaded file is checked against an embedded SHA-256 manifest. Existing local files and human entries are preserved. Public base models and the specified dataset are still loaded from Hugging Face in the cells below.

When opened within the repository, the existing workspace is used. Otherwise runtime files live in `p13_runtime/` beneath the current working directory. `P13_WORKSPACE` can set an explicit writable location. The GitHub artifact snapshot is pinned independently of the latest repository notebook, so later repository edits cannot silently change these saved weights.

The setup cell contains all dependency versions; no separately submitted `requirements.txt` is needed. Use a fresh kernel. First use requires internet and model-download time. `TRAIN=False` uses matching saved adapters; `TRAIN=True` retrains. `QUICK_RUN=True` evaluates 60 test emails; set `P13_QUICK_RUN=0` before Run All for the full 300-email run. Saved outputs below use the full run. Setup/download time and execution time are reported separately at the end.
'''
    sources[3] = f'''# AI-assisted portable setup; all executable support is embedded in this notebook.
import os, sys, time
from pathlib import Path
P13_NOTEBOOK_STARTED = time.perf_counter()
if sys.version_info < (3, 12):
    raise RuntimeError('Use Python 3.12 or newer for the pinned NumPy environment; Python 3.12 was tested.')
cwd = Path.cwd()
default_workspace = cwd if (cwd/'artifacts/revisions.json').exists() else cwd/'p13_runtime'
P13_ROOT = Path(os.environ.get('P13_WORKSPACE', str(default_workspace))).expanduser().resolve()
P13_ROOT.mkdir(parents=True, exist_ok=True)
PINNED_REQUIREMENTS = {pins!r}
requirements_path = P13_ROOT/'requirements.txt'
requirements_path.write_text(PINNED_REQUIREMENTS, encoding='utf-8')
%pip install -q -r "{{requirements_path}}"

SUBMISSION_SUPPORT_SOURCE = {support!r}
support_path = P13_ROOT/'submission_support.py'
support_path.write_text(SUBMISSION_SUPPORT_SOURCE, encoding='utf-8')
submission_support = {{'__name__':'p13_submission_support'}}
exec(compile(SUBMISSION_SUPPORT_SOURCE, str(support_path), 'exec'), submission_support)
ASSET_REPOSITORY = {REPOSITORY!r}
ASSET_REVISION = {REVISION!r}
SAVED_ASSET_MANIFEST = {json.dumps(manifest, indent=4)}
asset_setup = submission_support['ensure_submission_assets'](
    P13_ROOT, SAVED_ASSET_MANIFEST, ASSET_REPOSITORY, ASSET_REVISION)
P13_SETUP_SECONDS = time.perf_counter()-P13_NOTEBOOK_STARTED
print('Workspace:', P13_ROOT)
print('Saved asset snapshot:', ASSET_REVISION)
print('Existing files preserved:', asset_setup['existing_files_preserved'],
      '| downloaded and checksum-verified:', len(asset_setup['downloaded_files']))
'''
    sources[3] = sources[3].replace(f"PINNED_REQUIREMENTS = {pins!r}", 'PINNED_REQUIREMENTS = """'+pins+'"""')
    sources[3] = sources[3].replace(f"SUBMISSION_SUPPORT_SOURCE = {support!r}", "SUBMISSION_SUPPORT_SOURCE = r\'\'\'"+support+"\'\'\'")
    sources[4] = sources[4].replace('ROOT = Path.cwd()', 'ROOT = P13_ROOT')
    begin = sources[4].index('from huggingface_hub import HfApi')
    end = sources[4].index('\nenvironment = ', begin)
    sources[4] = sources[4][:begin] + f'''# Exact model/data revisions remain fixed even when only the notebook is supplied.
PINNED_REVISIONS = {revisions!r}
revision_path = ART/'revisions.json'
REVISIONS = json.loads(revision_path.read_text()) if revision_path.exists() else PINNED_REVISIONS.copy()
if REVISIONS != PINNED_REVISIONS:
    raise RuntimeError('Local revisions differ from the reviewed snapshot. Use a fresh P13_WORKSPACE.')
save_json(revision_path, REVISIONS)
''' + sources[4][end:]
    sources[4] = sources[4].replace("'device': DEVICE, 'dtype': str(DTYPE), 'quick_run': QUICK_RUN,", "'device': DEVICE, 'dtype': str(DTYPE), 'quick_run': QUICK_RUN,\n    'artifact_repository':ASSET_REPOSITORY, 'artifact_revision':ASSET_REVISION,\n    'setup_seconds':round(P13_SETUP_SECONDS,2),")

    sources[5] += '\n\nThe 4,000-email training cap is a fixed compute budget for the rank and defence comparisons, not a claim that the remaining emails are invalid. Stratified sampling preserves the approximately 62.7% safe / 37.3% phishing distribution. There is no learning-curve experiment establishing that 4,000 is optimal.\n'
    sources[9] += '''\n\n### Design decisions and simpler alternatives

| Decision | Simpler alternative and evidence |
| --- | --- |
| LoRA on a small open classifier | Compare unchanged zero-shot Qwen, keyword rules and kNN on the identical fixed test subset. The combined table reports both rank 4 and rank 8. |
| Training-only semantic retrieval | Compare k = 1, 3 and 5; choose k using validation F1. Retrieved labels are evidence, not verified campaign identity. |
| Fixed supervisor with separate roles | A sequential function pipeline would be sufficient for basic classification. LangGraph makes shared evidence, checkpointed approval and trace inspection explicit. We do not claim that the graph itself improves accuracy or implement autonomous planning. |
| Defence training plus two views and review rules | The security tables compare the original path, previous defence and current policy, with component ablations. Security gains have a measured clean-email false-positive cost. |
| Source-span selection in explanations | Compare against the original quote-copying method on the same validation emails. Exact quote checks are limited automatic checks; human quality still requires ratings. |
'''
    sources[29] += '\n\nThe active CSV is chosen by exact case/verdict/reason/quote matching. Historical ratings can be inspected in the repository archive, but they cannot establish the quality of revised explanations. Rater counts are computed from valid rows, never hard-coded. A first run creates a blank current sheet. Editing immutable text causes validation to fail rather than count scores for a different explanation.\n'
    begin = sources[30].index('rating_path = ')
    loop_begin = sources[30].index('rating_rows = []')
    loop_end = sources[30].index('expected_ratings = pd.DataFrame(rating_rows)')
    loop = sources[30][loop_begin:loop_end]
    sources[30] = "rating_base_path = (RUN if QUICK_RUN else ART)/'human_explanation_ratings.csv'\n" + loop + '''expected_ratings = pd.DataFrame(rating_rows)
rating_result = submission_support['load_current_ratings'](expected_ratings, rating_base_path)
rating_path = rating_result['path']
ratings, numeric_ratings, valid = (rating_result[name] for name in ['ratings','numeric','valid'])
if rating_result['preserved_path'] is not None:
    print('Preserved historical rating sheet:', rating_result['preserved_path'].relative_to(ROOT))
    print('Historical scores are not counted for the current explanations.')
print(f'Completed valid CURRENT human ratings: {int(valid.sum())}/{len(ratings)}')
print('Current rating sheet:', rating_path.relative_to(ROOT))
print('Rater counts from valid current rows:', rating_result['rater_counts'])
if int(valid.sum()) >= 30:
    display(pd.Series(rating_result['means'], name='mean_current_human_rating'))
else:
    print('Current explanation quality: pending 30 real human ratings; no scores are fabricated or transferred.')
component_metrics['human_ratings_status'] = 'complete' if int(valid.sum()) >= 30 else 'pending real human input'
component_metrics['human_ratings_completed'] = int(valid.sum())
component_metrics['human_rating_sheet'] = str(rating_path.relative_to(ROOT))
component_metrics['human_rating_snapshot_verified'] = True
component_metrics['human_rater_counts'] = rating_result['rater_counts']
component_metrics['mean_human_ratings'] = rating_result['means']
save_json(RUN/'component_metrics.json', component_metrics)
'''
    # Show score provenance and choose an informative observed success for the demo,
    # without changing any test outcome or using it for model/policy selection.
    sources[34] = sources[34].replace("    print('Reason:',output['explanation']['reason'])", "    print('Scores (uncalibrated A/B): original=',round(output['phishing_score'],4),\n          'structured=',round(output['structured_defence_score'],4),\n          'plain=',round(output['plain_defence_score'],4))\n    print('Explanation uses a visible template fallback:',output['explanation']['fallback_used'])\n    print('Reason:',output['explanation']['reason'])")
    old = "correct_indices = np.flatnonzero(PREDICTIONS['Full system (defended)']==truth)\nprint('Dataset label:',test_df.iloc[int(correct_indices[0])].label_name)\ndemo_success_thread = ask(test_df.iloc[int(correct_indices[0])].text)"
    new = '''correct_indices = np.flatnonzero(PREDICTIONS['Full system (defended)']==truth)
# Presentation selection only: prefer a true positive with a model explanation,
# no identical bounded training input, and no almost-identical retrieved example.
preferred_successes = [int(i) for i in correct_indices if truth[i] == 1
    and not input_overlap_mask[i] and not system_outputs[i]['explanation']['fallback_used']
    and max((e['similarity'] for e in system_outputs[i]['evidence']), default=0.) < .98]
phishing_successes = [int(i) for i in correct_indices if truth[i] == 1]
demo_success_index = (preferred_successes or phishing_successes or correct_indices.tolist())[0]
print('Selection: first observed correct phishing example with verified model quote and no near-copy, when available.')
print('This choice illustrates a result; it does not change the benchmark or tune the policy.')
print('Dataset label:',test_df.iloc[demo_success_index].label_name)
demo_success_thread = ask(test_df.iloc[demo_success_index].text)'''
    assert old in sources[34]
    sources[34] = sources[34].replace(old,new)
    sources[33] += '\n\nThe success example is chosen after evaluation only for presentation: prefer a correctly flagged phishing-labelled email with a nonfallback exact quote, no identical bounded training input and no retrieved similarity of 0.98 or more. The failure remains an observed full-system error. This presentation choice does not alter test membership, model weights, thresholds or reported metrics. The earlier deck illustrates its saved historical examples; live examples can differ under this explicit selection rule.\n'
    sources[35] += '\n- The submission setup retrieves pinned saved artifacts from the linked public repository and checks downloaded bytes. A first run still needs internet for dependencies, assets, the dataset and base models. Existing local files are preserved, and their adapter metadata is validated by the training/loading cells. The reviewed one-file workflow is tested separately from any permitted-device runtime claim.\n'
    sources[36] += '\n- Supporting results and presentation: [project GitHub repository](https://github.com/kaustubh-dot/Phishing_Email_Triage). Runtime assets are pinned to commit `'+REVISION+'`, with per-file SHA-256 values in Setup. The repository documents historical experiments separately from the current evaluation.\n'
    sources[37] = sources[37].replace('runtime_seconds = time.perf_counter()-STARTED', 'runtime_seconds = time.perf_counter()-STARTED\ntotal_runtime_seconds = time.perf_counter()-P13_NOTEBOOK_STARTED')
    sources[37] = sources[37].replace("'under_60_minutes':runtime_seconds < 3600,", "'setup_seconds':round(P13_SETUP_SECONDS,2),\n    'total_runtime_seconds':round(total_runtime_seconds,2),\n    'under_60_minutes':total_runtime_seconds < 3600,\n    'asset_revision':ASSET_REVISION, 'downloaded_asset_count':len(asset_setup['downloaded_files']),")
    sources[37] = sources[37].replace("'human_ratings_required':30,", "'human_ratings_required':30,'human_rating_snapshot_verified':True,\n    'human_rater_counts':rating_result['rater_counts'],")
    sources[37] += "\nprint(f'Total including this run setup: {total_runtime_seconds/60:.1f} minutes; first model download times depend on network/cache.')\nprint('Verified execution: all evaluation stages completed successfully on', environment.get('gpu') or DEVICE)\nprint('Final human checks: complete current ratings and team review. Classification and security limitations remain reported above.')\n"
    for cell,source in zip(cells,sources):
        cell['source'] = source.splitlines(keepends=True)
        if cell['cell_type']=='code':
            cell['execution_count']=None
            cell['outputs']=[]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(notebook,indent=1,ensure_ascii=False)+'\n')
    (args.output.parent/'source_provenance.json').write_text(json.dumps({
        'original_filename':args.source.name,'original_sha256':sha256(args.source.read_bytes()).hexdigest(),
        'reviewed_filename':args.output.name,'runtime_asset_revision':REVISION,
        'runtime_asset_count':len(manifest),'github_push_authorized':False,
    },indent=2)+'\n')
    print(args.output)


if __name__=='__main__':
    main()
