# Phase 3 review

Reviewer: GPT-6.1-sol, reasoning effort xhigh, independent subagent.

Scope: notebook cells `p13-014`, `p13-015`, `phase3-results`, the Phase 3 checkpoint, saved rank-8/rank-4 adapters and their metadata. Earlier reviewed source cells were preserved. Phase 4 was excluded.

Result: **Passed after direct corrections. No remaining blocking correctness findings for Phase 3.** The disclosed bounded-input overlap and statistical/generalization limits remain evaluation limitations, not a claim of fully independent classifier inputs.

## Corrections made before passing

- Fixed evaluation immediately after training. `Trainer` leaves a BF16 autocast wrapper on the model's forward method. Evaluating that object and later loading the saved adapter used different numerical paths, changing one test decision per rank. Both freshly trained and cached adapters now go through a fresh `PeftModel.from_pretrained` inference reload before scoring. The later primary classifier uses that same path. No weights, prompt or decision threshold were tuned or retrained during review.
- Fixed `TRAIN=True` causing rank 8 to train twice: final primary setup now explicitly requests a cached reload. Training reports contain one entry per rank.
- Strengthened cache provenance with hashes of all actual tokenized training/validation inputs and masked targets, label/EOS IDs, objective, dataset/model identities and explicit optimizer/scheduler defaults. Matching cached adapters also validate their LoRA configuration. A changed token fingerprint is rejected before a model load. Existing metadata was reconstructed against the reviewed original inputs/arguments; that provenance is explicitly marked rather than presented as originally recorded.
- Pinned the base model revision in each saved adapter configuration and future LoRA saves. The notebook already loads the base at its immutable recorded revision; standalone adapter loading now carries it too.
- Corrected the objective description: loss covers the A/B label **and EOS**, with the prompt and right padding masked. Added a LoRA-only trainability assertion.
- Disclosed one training/test pair that becomes identical after bounded Qwen preprocessing. Full normalized emails remain distinct. Preserved the reviewed fixed splits, and added a separate exclusion sensitivity table using the same eligible test emails for every condition. Updated the checkpoint, README and roadmap with the measured results and limitation.

## Independent verification

- All 4,400 training/validation examples have the expected prompt followed by exactly the correct single-token label and EOS. Prompt targets are `-100`; attention masks cover real tokens. Encoding prompt-plus-letter preserves the intended token boundary for every example.
- The collator right-pads inputs with EOS, masks padding in attention, and uses `-100` padding labels. Genuine EOS targets remain supervised. On a padded validation batch, manual next-token-shifted cross entropy equals the model loss exactly (0.0005084442673251033); exactly two targets per example contribute.
- Only q_proj/v_proj LoRA A/B parameters are trainable: rank 8 has 540,672 parameters and rank 4 has 270,336. A backward check produces finite nonzero adapter gradients and no frozen-base gradients; no optimizer step was performed.
- Each saved adapter contains 96 finite, nonzero LoRA tensors, with the expected parameter count and module names. Saved tokenizer vocabulary, chat template and special tokens match the pinned base tokenizer. Adapter weights were not modified.
- Both ranks use identical 4,000 training / 400 validation examples, seed/data_seed 42, one epoch, batch size 8, 500 optimizer steps, learning rate 0.0002, linear scheduling, dropout 0.05, no warmup and alpha/rank = 2. Validation loss is an evaluation of the label-plus-EOS objective; rank 8 was predeclared primary, not selected on test results.
- The original numerical discrepancy was isolated on the same saved weights: BF16 autocast reproduces all original 300 test decisions for each rank; default adapter inference differs at one case per rank. Rank 8's safe case score changes 0.592667 → 0.468791, removing one false positive. Rank 4's phishing case score changes 0.407333 → 0.592667, removing one false negative. The diagnostic is saved as `artifacts/results/full/phase3_precision_diagnostic.json`.
- Executed the full current notebook from a fresh CUDA kernel, with cached matching adapters, in **25.8 seconds**. All eight code cells have successful saved outputs. Notebook format and code syntax validate. The initial training run's recorded runtimes remain 157.11 / 157.62 seconds; review did not retrain.
- In a separate GPU process, the actual `train_or_load(..., retrain=False)` path independently reproduced **all 300 final predictions for both ranks**. Reloads are frozen and in evaluation mode, including when the global `TRAIN` flag is True. The primary cache is populated from this same inference path. Phase 2's explicit mask-derived inference position IDs remain intact.
- Independently recalculated every metric in both the full 300-message table and the matched 299-message sensitivity table from the saved predictions. Checks are saved in `artifacts/results/full/phase3_review_checks.json`.

## Authoritative saved-adapter results

Rows in confusion matrices are true safe/phishing; columns are predicted safe/phishing.

| Condition | Confusion matrix | Accuracy | Precision | Recall | F1 | False-positive rate |
| --- | --- | --- | --- | --- | --- | --- |
| LoRA rank 8 (primary) | `[[185, 3], [4, 108]]` | 0.976667 | 0.972973 | 0.964286 | 0.968610 | 0.015957 |
| LoRA rank 4 | `[[186, 2], [7, 105]]` | 0.970000 | 0.981308 | 0.937500 | 0.958904 | 0.010638 |
| Validation-selected k=5 | `[[182, 6], [5, 107]]` | 0.963333 | 0.946903 | 0.955357 | 0.951111 | 0.031915 |

Keyword and unchanged zero-shot results remain the reviewed Phase 2 results (F1 0.130081 / 0). The initial Trainer-wrapped LoRA F1 values 0.964286 / 0.954128 are retained as diagnostic history, not presented as final deployed-path results.

## Remaining limitations

One safe test email (`5f900787…`) and a distinct safe training email (`a699f247…`) have identical bounded classifier inputs despite different normalized full texts (18,873 versus 11,103 characters). There are no identical bounded train/validation or validation/test prompts in the audited comparison. The overlap is saved in `classifier_input_overlap.json`. Removing that test case from every condition leaves 299 matched examples: rank-8 F1 stays 0.968610, rank-4 F1 becomes 0.963303 and selected k=5 F1 stays 0.951111. The excluded case was a rank-8 true negative but a rank-4 false positive. The original 300-message comparison remains primary and explicitly includes this overlap.

Exact full-text deduplication does not eliminate remaining near duplicates, dataset-specific style cues or possible pretraining exposure. Truncation can hide decisive evidence. This is one seed, one small held-out subset and broad safe/phishing labels that include spam/scams; the F1 difference is not evidence of statistical significance or real-world reliability. A/B-normalized scores are not calibrated probabilities, and the observed precision sensitivity demonstrates that numerical settings can affect individual decisions. These limitations must remain in the final evaluation narrative.

Phase 3 is released. Phase 4 may begin.
