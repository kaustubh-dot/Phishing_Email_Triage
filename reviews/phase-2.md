# Phase 2 review

Reviewer: GPT-6.1-sol, reasoning effort xhigh, independent subagent.

Scope: notebook cells `p13-009` through `p13-011`, their checkpoint narrative and saved Phase 2 results. LoRA training and later phases were excluded.

Result: **Passed. No remaining blocking or actionable correctness findings.**

## Corrections made before passing

- Added model ID, revision, character cap, maximum embedding sequence length and normalization settings to the embedding cache key. Changing those settings can no longer silently reuse incompatible cached vectors. Added vector shape, finiteness and unit-norm checks.
- Made mask-derived position IDs explicit for left-padded Qwen batches and disabled the unused inference cache. Final-position A/B logits were already indexed correctly; the label IDs are 32 (`A`) and 33 (`B`), and appending either letter to the chat generation prefix preserves that tokenization.
- Documented constrained raw next-token classification, the unchanged 0.5 decision threshold, character/token truncation, embedding truncation and the absence of probability calibration. The prompt and threshold were not tuned.
- Added a validation-only comparison of batched scoring, individual scoring and one-token greedy generation with repetition penalty disabled. Saved the check as `artifacts/results/full/phase2_scoring_check.json`.
- Displayed and saved a fixed validation retrieval example with training source IDs, labels, cosine similarities and excerpts in `artifacts/results/full/retrieved_evidence_example.json`.
- Updated Phase 2 checkpoint, README and roadmap to report the measured baseline failure and the validation-selected retrieval result.

## Independent verification

- Executed the entire current notebook from a fresh kernel on the NVIDIA RTX 4000 Ada GPU with `P13_QUICK_RUN=0`. Execution completed in 18.7 seconds with successful saved outputs and no error outputs. Notebook format and code syntax validate.
- The FAISS index contains exactly the 4,000 training embeddings. Query labels are not supplied to retrieval. Index sources are disjoint from validation and test IDs; the saved demonstration query belongs to validation and every retrieved source belongs to training.
- Independently reconstructed query text from the cached dataset and saved split manifest. Compared FAISS top-five cosine scores against brute-force NumPy inner products for all 400 validation and 300 test queries. Scores agree within `1e-6`; a few equal-score neighbors have different ordering, as expected for ties. All saved kNN test predictions reproduced exactly.
- Independently reproduced validation F1: k=1, 0.923588; k=3, 0.936877; k=5, 0.937705. Selection chooses k=5 using validation only. The separate test ablations do not change that choice.
- Reproduced label-agreement Hit@5 = 0.983333 and reciprocal rank at 5 = 0.970000. They are correctly identified as label proxies rather than judged semantic relevance metrics.
- Independently recalculated every saved classification metric from `predictions.csv`. Confusion matrices, with true safe/phishing as rows and predicted safe/phishing as columns, are: keyword `[[185, 3], [104, 8]]`; k=1 `[[181, 7], [5, 107]]`; k=3 `[[183, 5], [5, 107]]`; selected k=5 `[[182, 6], [5, 107]]`; zero-shot `[[188, 0], [112, 0]]`.

## Zero-shot diagnostic finding

The all-safe result is real under this fixed prompt and constrained scoring method. Four fixed validation examples, two from each class, have matching batched, individual and neutral greedy-generation decisions. BF16 batched/individual scores differ by at most 0.013762 on these examples without changing decisions. The full test phishing-score range after the correction is 0.014064–0.377541; none reaches 0.5. No test-set prompt search or threshold adjustment was performed.

The cached Qwen generation configuration has repetition penalty 1.1. An initial diagnostic using that generation default produced a different decision on one validation example even though the raw logits preferred `A`: the penalty can lower a letter that already appears in the prompt. Disabling that penalty makes generation agree with raw next-token scoring. This is a method distinction, not an A/B indexing or parsing bug. The notebook states which method it evaluates.

Selected k=5 test accuracy is 0.963333, precision 0.946903, recall 0.955357, F1 0.951111 and false-positive rate 0.031915. Unchanged zero-shot Qwen has accuracy 0.626667, phishing recall/F1 0 and 112 false negatives. The notebook preserves this poor result and identifies it as unsuitable for a standalone phishing decision. Long-input truncation, broad spam/scam labels and dataset-specific similarity remain evaluation limitations; these measurements do not establish performance on new real-world mail.

No LoRA training or later-phase implementation was performed during this review. Phase 3 may begin.
