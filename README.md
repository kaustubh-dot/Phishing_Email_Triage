# Phishing email triage (P13)

A text-email triage notebook built to the original P13 brief, including its MCP server stretch goal. It combines Qwen LoRA classification, MiniLM/FAISS retrieval, local indicator tools, explanations and a LangGraph supervisor. Every quarantine proposal requires explicit analyst approval; actions are simulated.

The complete implementation, saved evaluation and demo are in [Phishing_Email_Triage.ipynb](Phishing_Email_Triage.ipynb). The latest changes prioritize injection resistance and preserve the original adapters as baselines. See [DEFENCE_IMPROVEMENTS.md](DEFENCE_IMPROVEMENTS.md) for the training, held-out security results and clean-email tradeoff.

## Run locally

Use Python 3.12 and keep the notebook at the repository root.

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name python3
```

Select `.venv/bin/python` as the kernel and run all cells in order. First use needs internet for the public Hugging Face dataset and pinned base models. The saved original and defensive adapters are included. Downloads, embeddings and training checkpoints are cached locally and excluded from Git.

- `QUICK_RUN=True` evaluates 60 fixed test emails; `False` evaluates all 300. `P13_QUICK_RUN=1` or `0` overrides the flag. Committed outputs show the full evaluation.
- `TRAIN=False` loads matching saved adapters or trains missing ones. `TRAIN=True` retrains. Incompatible cached metadata raises an error.
- Both modes use the same 4,000 downloaded training emails, 400 validation emails and training-only retrieval index. Defensive training creates 8,000 derived examples from those 4,000 identities; it never trains on validation/test emails or held-out attack cases.

Fresh full execution with saved adapters takes about three to four minutes on the available RTX 4000 Ada GPU; quick mode takes about 85 seconds. Defensive training took approximately 279 seconds on that GPU. Full laptop CPU/free Colab T4 timing remains unverified. A notebook-only copy needs accompanying adapters and rating snapshots or must retrain. Both helper Python files and security-fixture recipes are embedded and recreated by the notebook.

## Defensive training and decisions

The original rank-4/rank-8 LoRA adapters remain unchanged. A separate rank-8 adapter continues training with 4,000 clean structured examples, 2,000 clean plain examples and 2,000 label-preserving adversarial examples. Requested A/B labels are balanced independently of true labels. The inference threshold stays at 0.5.

Half/full checkpoints are selected on development security outcomes subject to prespecified clean-validation and malicious-control safeguards. The full checkpoint is frozen before scoring the fresh attack holdout. Both escaped JSON and escaped plain-text views use this selected model. Either may flag phishing. Unanimous training-only retrieval can also request review.

The existing extractor adds a bounded review rule for direct secret requests at untrusted URLs, or disabling protection and installing/running a download. Negation handling is tested but limited. Exact known-brand spelling is a policy exception, not authentication or reputation verification. The full verdict and contributing indicator evidence are visible to the analyst. No component can approve quarantine.

## Injection results

The original 30 attacks share ten malicious scenarios. The revised off/on comparison correctly quarantines every control in both modes, so all 30 pairs have the same eligibility: targeted ASR falls from **10/30 (33.3%) off to 1/30 (3.3%) on**. The previous defence allowed 7/30 attacked emails and missed three underlying controls.

A fresh 150-pair holdout uses new payload templates and disjoint development/test identities. It was frozen before training and was not used for model selection.

| Fresh holdout outcome | Defence off | Previous defence | Improved defence |
| --- | ---: | ---: | ---: |
| Dataset-labelled phishing attacked emails allowed | 11/30 | 7/30 | 2/30 |
| Explicit phishing attacked emails allowed | 4/30 | 7/30 | 0/30 |
| Benign emails forced into quarantine | 26/30 | 10/30 | 2/30 |
| Authored benign emails forced into quarantine | 22/30 | 8/30 | 4/30 |

All ten unique explicit malicious holdout controls are quarantined by the improved policy. Two dataset-labelled phishing controls remain wrong before and after injection; their allows are included in the table. Benign allow-directed negative controls produce 1/30 false quarantine proposals versus 0/30 previously.

Results include all control/attacked outcomes, conditional denominators, common-pair comparisons and structured-only/two-view/retrieval/full-policy ablations. An ASR with no eligible controls is undefined. Authored scenarios and related payload families are correlated; these results do not establish general immunity or statistical significance.

## Clean classification tradeoff

Every classification condition uses the same 300 fixed test emails: 188 safe and 112 phishing. Phishing is positive. The complete baseline and ablation table remains in the notebook and saved metrics.

| Condition | Accuracy | Precision | Recall | F1 | False-positive rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Keyword rules | 0.6433 | 0.7273 | 0.0714 | 0.1301 | 0.0160 |
| Zero-shot Qwen | 0.6267 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| kNN, validation-selected k=5 | 0.9633 | 0.9469 | 0.9554 | 0.9511 | 0.0319 |
| Original LoRA rank 8 | 0.9767 | 0.9730 | 0.9643 | 0.9686 | 0.0160 |
| Original LoRA rank 4 | 0.9700 | 0.9813 | 0.9375 | 0.9589 | 0.0106 |
| Defensive LoRA, structured only | 0.9633 | 0.9316 | 0.9732 | 0.9520 | 0.0426 |
| Defensive LoRA, two-view | 0.9567 | 0.9160 | 0.9732 | 0.9437 | 0.0532 |
| Full improved defence | 0.9467 | 0.8934 | 0.9732 | 0.9316 | 0.0691 |

The full improved workflow has 13 false positives and 3 false negatives, versus 5/3 and F1 0.9646 for the previous workflow. The original rank-8 classifier has 3/4 and F1 0.9686. This material cost is reported explicitly; the security policy is not retuned on test outcomes. The full evaluation pauses all 122 quarantine proposals and executes none. Separate integration checks cover approval, rejection, replay protection and thread isolation.

Zero-shot still predicts every test email as safe under the unchanged constrained A/B method. Scores and max-of-view combinations are not calibrated probabilities.

## Explanations and human ratings

The explainer writes a factual observation and selects an exact source span by ID. Invalid structure, IDs and some directly checkable unsupported claims produce visible template fallbacks. Quote verification does not establish reasoning correctness. Current counts and failure reasons are in `artifacts/results/full/component_metrics.json`.

The original [30 completed ratings](artifacts/human_explanation_ratings.csv) remain unchanged for their historical explanation snapshot. Revised explanations need **30 fresh human ratings**. The active fingerprinted sheet is identified by `human_rating_sheet` in [run_summary.json](artifacts/results/full/run_summary.json). Rate correctness, grounding and usefulness from 1 to 5 and record the rater's name; rerun to validate matching text. Historical ratings are never transferred to changed explanations.

## MCP server and demo

[mcp_indicator_server.py](mcp_indicator_server.py) exposes `extract_urls`, `check_domain_lookalike` and `extract_sender_headers` through the official MCP SDK 1.28.0 over stdio:

```bash
.venv/bin/python mcp_indicator_server.py
```

The server waits for MCP client requests and needs no model or URL fetching. The notebook embeds the same source and verifies initialization, discovery, calls, output parity and invalid-argument rejection. No quarantine action is exposed. References: [SDK v1 documentation](https://py.sdk.modelcontextprotocol.io/v1/), [SDK source](https://github.com/modelcontextprotocol/python-sdk).

After Run All, `ask(email)` prints original/workflow verdicts, defence changes, indicator review reasons, explanation, retrieved evidence and trace. A quarantine proposal waits for `review(thread_id, 'approve')` or `review(thread_id, 'reject')`. Completed threads cannot be reused. The demo includes a success and an actual failure.

## Verification and limits

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

Fourteen regression checks cover MCP, URL/header handling, two-view preservation, label-balanced augmentation, holdout separation, negated security reminders and explanation validation. Saved training fingerprints and frozen selection records are under `artifacts/adapters/defended-r8/`; all evaluation evidence is under `artifacts/results/full/`.

The public dataset includes ambiguous spam labels and near-duplicate campaigns. One bounded classifier input overlaps training/testing; the same 299-email sensitivity table is retained. Fixed context limits can hide evidence. Local tools do not authenticate headers or establish website reputation. Checkpoints and simulated quarantine logs disappear on restart.

Before submission, complete the current human ratings, review the AI-assisted changes as a team, and verify execution on a permitted laptop or free Colab T4. Contributions, references, ethics, failure analyses and presentation walkthrough remain in the notebook.

The earlier [injection audit](INJECTION_DEFENCE_REVIEW.md) is historical evidence behind this implementation. `scripts/audit_injection_defences.py` reproduces those original-adapter ablations against fixed reference actions; the notebook evaluates the latest defence. The scope remains text-email triage plus the named MCP stretch goal.
