# Phishing email triage (P13)

A text-email triage notebook built to the P13 brief, including its MCP server stretch goal. It combines a Qwen LoRA classifier, MiniLM/FAISS retrieval, local indicator tools, model explanations and a LangGraph supervisor. Every quarantine proposal requires an explicit analyst decision; actions are simulated.

The complete implementation, saved evaluation and live demo are in [Phishing_Email_Triage.ipynb](Phishing_Email_Triage.ipynb). This revision improves the injection regression results and reduces explanation fallbacks, with a disclosed false-positive tradeoff. Team review and 30 fresh human ratings of the revised explanations remain necessary before submission.

## Run locally

Use Python 3.12 and keep the notebook at the repository root.

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name python3
```

Open the notebook, select `.venv/bin/python`, and run all cells in order. The first run needs internet for the specified Hugging Face dataset and base models. Dependencies and dataset/model revisions are pinned. Both saved LoRA adapters are included; downloaded models/data and embeddings are cached locally and excluded from Git.

- `QUICK_RUN=True` evaluates 60 fixed test emails; `False` evaluates all 300. `P13_QUICK_RUN=1` or `0` overrides the flag. Committed outputs show the full evaluation.
- `TRAIN=False` loads matching saved adapters or trains once if they are absent. `TRAIN=True` retrains both ranks. Mismatching adapter metadata raises an error.
- Both modes use the same 4,000 training emails, 400 validation emails and training-only retrieval index, with seed 42.

Fresh full execution has been verified on the available NVIDIA RTX 4000 Ada GPU in approximately three minutes. Full laptop CPU and free Colab T4 timing remain unverified. The notebook uses CUDA when available and otherwise CPU. A notebook-only copy needs the accompanying adapters and ratings or must retrain; the complete MCP server source is embedded and recreated by the notebook.

## Classification and decision policy

All conditions below use the same 300 test emails: 188 safe and 112 phishing. Phishing is positive. k=5 is selected using validation F1; k=1/3 and LoRA rank 4 are reported as ablations.

| Condition | Accuracy | Precision | Recall | F1 | False-positive rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Keyword rules | 0.6433 | 0.7273 | 0.0714 | 0.1301 | 0.0160 |
| Zero-shot Qwen | 0.6267 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| MiniLM/FAISS kNN, k=5 | 0.9633 | 0.9469 | 0.9554 | 0.9511 | 0.0319 |
| LoRA rank 8 | 0.9767 | 0.9730 | 0.9643 | 0.9686 | 0.0160 |
| LoRA rank 4 | 0.9700 | 0.9813 | 0.9375 | 0.9589 | 0.0106 |
| Full defended workflow | 0.9733 | 0.9561 | 0.9732 | 0.9646 | 0.0266 |

The raw LoRA threshold remains 0.5. Validation compares LoRA alone against policies that also propose phishing when 3, 4 or 5 of five training neighbors are phishing. Unanimous 5/5 corroboration wins on validation F1: 0.9568 versus 0.9452 for LoRA alone. Selection never uses test labels.

On the test set, this policy corrects one LoRA false negative but introduces two false positives. Full-system recall improves, while accuracy and F1 fall slightly. LoRA alone has three false positives/four false negatives; the full workflow has five/three. The new errors include ordinary discussions about scams and account cancellation. Their analyses are saved explicitly. No policy change is made to hide this test tradeoff.

Raw LoRA verdicts and workflow verdicts remain separate in graph state. Retrieval cannot downgrade a phishing verdict, and a retrieval override cannot bypass human approval. The full workflow pauses all 114 quarantine proposals and executes none during evaluation. Approval, rejection, replay protection and thread isolation are checked independently.

The unchanged zero-shot model still predicts every test email as safe under constrained A/B scoring. Those two-token scores are not calibrated probabilities.

## Injection regression results

Thirty payloads share ten authored malicious scenarios. Each is paired with its unmodified control. The notebook reports raw allow rates, eligible-control denominators, classifier flips and retrieval overrides.

| Current run | Defence off | Defence on |
| --- | ---: | ---: |
| Attacked emails allowed, all 30 pairs | 10/30 | 7/30 |
| Targeted successes, same 21 common-eligible pairs | 6/21 (28.6%) | 4/21 (19.0%) |
| Malicious controls allowed, all 30 repeated controls | 0/30 | 9/30 |

The previous submission allowed 15/30 attacked emails with defence enabled. The revised workflow allows 7/30, but three of ten underlying malicious controls still receive allow proposals. Defence on bundles untrusted-data boundaries, chat-delimiter escaping, validation-selected retrieval corroboration, responder shielding and action consistency.

This suite was inspected during development and is now a regression stress test. Its payloads are correlated; it is not an unseen security benchmark. Old and new conditional ASRs have different eligible denominators and must not be compared directly. These observations establish neither general injection robustness nor statistical significance.

## Explanations and human ratings

The explainer writes a factual observation and selects a quote ID from exact email spans. Code resolves that ID to the original text. Invalid JSON, invalid IDs and some directly checkable unsupported claims produce visible fallbacks. The checks cannot establish full reasoning correctness.

On the same 16 fixed validation emails, the original quote-copying method passes format/quote checks on 7/16; span selection with stricter factual checks passes on 12/16. In the full revised evaluation, 226/300 explanations pass and 74/300 use templates, versus 142/300 and 158/300 previously. The validation methods have different checks, so these counts are not human quality scores.

The original [30 completed human ratings](artifacts/human_explanation_ratings.csv) are preserved unchanged for their historical snapshot. The revised run creates a separate fingerprinted sheet, identified in [run_summary.json](artifacts/results/full/run_summary.json). Its human fields are intentionally blank. Have team members rate correctness, grounding and usefulness from 1 to 5 and record their rater names. Rerun the notebook to count only ratings matching the exact current text. Historical scores must not be transferred to revised explanations.

## MCP server stretch goal

[mcp_indicator_server.py](mcp_indicator_server.py) exposes three local tools through the official MCP Python SDK 1.28.0 over stdio:

- `extract_urls`: explicit, common defanged and spaced HTTP(S) URLs.
- `check_domain_lookalike`: limited brand lookalikes and deceptive URL userinfo.
- `extract_sender_headers`: unauthenticated sender claims from leading headers.

Start it with:

```bash
.venv/bin/python mcp_indicator_server.py
```

The server waits for an MCP client's requests on stdin/stdout. It needs no model, dataset download, mailbox or URL fetching. The notebook embeds the same complete source and recreates the file, so its LangChain wrappers and the MCP tools share one implementation. A real stdio client verifies initialization, discovery, all three calls, output parity and invalid-argument rejection. No quarantine action is exposed through MCP.

References: [official SDK v1 documentation](https://py.sdk.modelcontextprotocol.io/v1/), [Python SDK source](https://github.com/modelcontextprotocol/python-sdk).

## Demo and verification

After running the notebook, `ask(email)` prints raw and workflow verdicts, the retrieval override, explanation, indicators, evidence and trace, then returns a fresh thread ID. A quarantine waits for `review(thread_id, 'approve')` or `review(thread_id, 'reject')`. Completed threads cannot be reused. The demo includes an actual success and failure.

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

Eight regressions cover MCP protocol behavior, URL handling, header isolation, retrieval policy boundaries, quote selection and unsupported claims. Notebook integration checks cover the full approval boundary. Metrics, predictions, validation selections, charts, injection details and failure analysis are saved under `artifacts/results/full/`.

## Limits and submission work

Exact normalized IDs are disjoint, but one training/test pair becomes identical after classifier truncation; a common 299-email sensitivity table is included. Independent inspection found additional near-copy train/test messages. The original split is preserved; results do not establish generalization across email campaigns.

Tools perform local text analysis with a limited brand list. They do not authenticate senders or establish URL reputation. Fixed input limits can hide evidence. Checkpoints and simulated quarantine logs disappear on kernel restart.

Before submission, complete 30 ratings for the revised snapshot, review the AI-assisted changes as a team, and verify the notebook on a permitted laptop or free Colab T4. Team contributions, ethics, lab adaptations and references remain in the notebook. QR/image processing, online learning and mailbox integration are outside scope.
