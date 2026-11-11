"""Check real CPU LoRA training, saving and reloading without changing benchmark adapters.

Runs the notebook's own data preparation, tokenization, collator and training
function in a temporary workspace. The check uses eight training emails, four
validation emails and one optimizer step; it is not a full retraining experiment.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir', type=Path, default=ROOT/'.cache/huggingface')
    parser.add_argument('--output', type=Path, default=ROOT/'output/submission/verification/cpu_training_smoke.json')
    args = parser.parse_args()
    notebook = json.loads((ROOT/'Phishing_Email_Triage.ipynb').read_text(encoding='utf-8'))
    sources = [''.join(cell['source']) for cell in notebook['cells']]
    asset_source = '\n'.join('pass' if line.lstrip().startswith('%') else line
                             for line in sources[3].splitlines())
    assets = {node.targets[0].id: ast.literal_eval(node.value)
              for node in ast.parse(asset_source).body
              if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
              and node.targets[0].id in {'ASSET_REPOSITORY', 'ASSET_REVISION'}}
    weights = [ROOT/f'artifacts/adapters/{rank}/adapter_model.safetensors'
               for rank in ['r4', 'r8', 'defended-r8']]
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in weights}
    cache_parent = (ROOT/'.cache').resolve()
    assert cache_parent.is_relative_to(ROOT.resolve())
    cache_parent.mkdir(exist_ok=True)
    os.environ.update(P13_DEVICE='cpu', P13_QUICK_RUN='1',
        P13_HF_HOME=str(args.cache_dir.resolve()), HF_HUB_OFFLINE='1', HF_DATASETS_OFFLINE='1',
        MPLBACKEND='Agg', PYTHONUTF8='1')
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='cpu-training-', dir=cache_parent) as directory:
        work = Path(directory).resolve()
        assert work.is_relative_to(cache_parent)
        namespace = {'P13_ROOT': work, 'P13_SETUP_SECONDS': 0,
                     'display': lambda *values, **kwargs: None, **assets}
        exec(compile(sources[4], '<notebook setup>', 'exec'), namespace)
        exec(compile(sources[6], '<notebook data preparation>', 'exec'), namespace)
        namespace['train_df'] = namespace['train_df'].groupby('label', group_keys=False).head(4).copy()
        namespace['val_df'] = namespace['val_df'].groupby('label', group_keys=False).head(2).copy()
        assert len(namespace['train_df']) == 8 and len(namespace['val_df']) == 4
        namespace['DATA_FINGERPRINT'] = namespace['digest'](
            ''.join(namespace['train_df'].email_id)+''.join(namespace['val_df'].email_id))
        prefix = sources[11].split('base_model = load_classifier_base()')[0]
        exec(compile(prefix, '<notebook classifier functions>', 'exec'), namespace)
        prefix = sources[16].split('CLASSIFICATION_CACHE = {}')[0]
        exec(compile(prefix, '<notebook training functions>', 'exec'), namespace)
        original_arguments, original_trainer = namespace['TrainingArguments'], namespace['Trainer']
        observed = {}
        def one_step_arguments(**kwargs):
            kwargs.update(max_steps=1, eval_strategy='no')
            return original_arguments(**kwargs)
        class ObservedTrainer(original_trainer):
            def train(self, *values, **kwargs):
                result = super().train(*values, **kwargs)
                observed['optimizer_steps'] = self.state.global_step
                observed['lora_update_observed'] = any(
                    '.lora_B.' in name and bool(parameter.detach().abs().sum().item())
                    for name, parameter in self.model.named_parameters())
                return result
        namespace.update(TrainingArguments=one_step_arguments, Trainer=ObservedTrainer)
        model = namespace['train_or_load'](8, retrain=True)
        assert observed['optimizer_steps'] == 1 and observed['lora_update_observed']
        scores = namespace['score_prompts'](model, namespace['tokenizer'],
            [namespace['classifier_prompt'](text) for text in namespace['train_df'].text.head(2)],
            namespace['LABEL_IDS'])
        assert namespace['np'].isfinite(scores).all()
        report = {'device': namespace['DEVICE'], 'dtype': str(namespace['DTYPE']),
            'training_examples': 8, 'validation_examples': 4, 'batch_size': 8,
            **observed, 'checkpoint_reload_succeeded': True, 'full_retraining_performed': False,
            'configuration_overrides': {'max_steps': 1, 'eval_strategy': 'no'},
            'scope': 'CPU forward/backward, optimizer update, adapter save and reload using notebook code; not a full benchmark retraining.',
            'source_cells_sha256': hashlib.sha256(json.dumps(sources).encode()).hexdigest(),
            'training_email_ids': namespace['train_df'].email_id.tolist(),
            'versions': namespace['TRAINING_REPORTS'][0]['training_versions'],
            'wall_seconds': round(time.monotonic()-started, 2)}
        del model
        namespace.clear()
        import gc
        gc.collect()
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == before[str(p)] for p in weights)
    report['benchmark_adapters_unchanged'] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
