# Phishing Email Triage - P13

A self-contained notebook with Qwen LoRA classification, training-only MiniLM/FAISS retrieval, local indicator tools, an explainer/responder team and a LangGraph supervisor. Every quarantine proposal pauses for explicit analyst approval. Actions are simulated.

## Final submission

- [Canonical notebook with saved outputs](Phishing_Email_Triage.ipynb).
- [Submission status](SUBMISSION_STATUS.md) and [final review](docs/FINAL_SUBMISSION_REVIEW.md).
- [Presentation](output/presentations/P13_Phishing_Triage_Updated.pptx), [ten-minute script](output/presentations/TEN_MINUTE_SCRIPT.md), [runbook](output/presentations/TEN_MINUTE_RUNBOOK.md) and [extended study script](output/presentations/P13_Phishing_Triage_Full_Presentation_Script.md).

Submit the notebook or the exact `fix/review-data-attribution` branch. The repository's default `main` branch is an earlier version.

[Open this submission in Colab](https://colab.research.google.com/github/kaustubh-dot/Phishing_Email_Triage/blob/fix/review-data-attribution/Phishing_Email_Triage.ipynb). Select a T4 runtime when available and Run All to obtain actual target-device evidence.

The notebook preserves the owner's supplied complete GPU execution: **21 executed code cells, 300 test emails, no saved error outputs, 194.9 seconds excluding dependency installation** on NVIDIA RTX 4000 Ada. Its classifier, retrieval, explanation-generation and security logic match that supplied run. Portable setup, Windows MCP handling, human-review reporting and a factual analysis correction were updated afterward and checked separately. These edits do not claim a new full model run or a measured T4 runtime.

## Human-based reviews

**30 human-based reviews are complete, personally completed by the project owner.** [Case-level records](artifacts/human_based_reviews.csv) include the exact emails, verdicts, reasons, quotes, reviewer and completed status. [The confirmation](artifacts/human_review_confirmation.json) records the owner's confirmation and snapshot hash. The loader counts them only when all immutable explanation fields match; a new generated snapshot does not inherit the reviews.

The original numeric rating sheet is retained as a historical comparison. Its 30 human-based ratings have mean correctness **4.43**, grounding **4.37** and usefulness **3.63** out of five. Those means apply only to the original explanations. No new numeric means are inferred from the owner's completion confirmation. See [review-record details](docs/HUMAN_REVIEW.md) and [the reproducible summary](artifacts/results/full/human_rating_summary.json).

## Run locally

Use an isolated Python 3.12 environment. Windows PowerShell:

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name p13-triage
```

Select `.venv\Scripts\python.exe` as the notebook interpreter. Linux:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name p13-triage
```

Run all cells in order. A standalone notebook writes its pinned dependencies and embedded helpers and retrieves missing saved assets from an immutable public Git revision with SHA-256 checks. Existing local adapters and review entries are preserved. First use requires internet for dependencies, saved assets, pinned Hugging Face models and the specified dataset. Downloads, embeddings, virtual environments and intermediate checkpoints are excluded from Git.

- `QUICK_RUN=False` evaluates the fixed 300-email subset by default. `P13_QUICK_RUN=1` selects the fixed 60-email subset.
- `P13_DEVICE=cpu`, `cuda` or `auto` selects the backend. CUDA uses the supported BF16/FP16 path; CPU uses float32 and smaller inference batches. Full CPU generation can be slow.
- `TRAIN=False` loads matching saved adapters; missing adapters are trained. `TRAIN=True` retrains. Incompatible metadata fails clearly.
- Seed 42; 4,000 training, 400 validation and 300 full-test emails; training-only retrieval. The defensive adapter uses 8,000 derived examples from the 4,000 training identities, never validation/test identities.

The saved full timing is an RTX 4000 Ada measurement with caches and saved adapters. A separate real one-step CPU training/save/reload check passes. An earlier partial CPU run is archived; complete laptop CPU/free Colab T4 timing has not been certified. Confirm any target-device deadline on the actual presentation runtime.

## Saved evaluation

Every condition uses the same 300 emails: 188 safe and 112 phishing. Phishing is positive.

| Condition | Accuracy | Precision | Recall | F1 | False-positive rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Keyword rules | 0.6433 | 0.7273 | 0.0714 | 0.1301 | 0.0160 |
| kNN k=1 | 0.9600 | 0.9386 | 0.9554 | 0.9469 | 0.0372 |
| kNN k=3 | 0.9667 | 0.9554 | 0.9554 | 0.9554 | 0.0266 |
| kNN k=5 | 0.9633 | 0.9469 | 0.9554 | 0.9511 | 0.0319 |
| Zero-shot Qwen | 0.6267 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| LoRA r=8 | 0.9767 | 0.9730 | 0.9643 | 0.9686 | 0.0160 |
| LoRA r=4 | 0.9700 | 0.9813 | 0.9375 | 0.9589 | 0.0106 |
| Defensive LoRA (structured) | 0.9633 | 0.9316 | 0.9732 | 0.9520 | 0.0426 |
| Defensive LoRA (two-view) | 0.9567 | 0.9160 | 0.9732 | 0.9437 | 0.0532 |
| Full system (defended) | 0.9467 | 0.8934 | 0.9732 | 0.9316 | 0.0691 |

The full workflow has **13 false positives and 3 false negatives**. Original rank-8 has **3 false positives and 4 false negatives**. Stronger injection resistance has a clean-email false-positive cost; no thresholds or weights were changed in response to scored test results.

The original regression suite has 30 variants across ten malicious scenarios. The same 30 controls are eligible in both modes: targeted ASR is **10/30 off versus 1/30 on**. A separate frozen 150-pair holdout reports all outcomes, control accuracy, eligible denominators and component ablations. These correlated stress tests do not establish general injection immunity.

The saved explainer produces **223/300** outputs passing schema, exact-span and limited factual checks; **77/300** use visible template fallbacks. All 300 displayed quotes match source text. On 16 validation emails, the saved span-selection method accepts 13 outputs and falls back on three. These checks do not establish semantic correctness. Additional copy/word-budget diagnostics are available for human review; they do not retroactively change the supplied run's acceptance criteria.

The notebook reports ten detailed failures, a disclosed bounded-input overlap with a common 299-email sensitivity table, ambiguity in spam-like labels, near-copy campaigns and fixed context limits.

## MCP and demo

`mcp_indicator_server.py` exposes `extract_urls`, `check_domain_lookalike` and `extract_sender_headers` over the official MCP SDK's stdio transport. Tools parse local strings; they do not visit URLs, authenticate senders or establish website reputation. The notebook embeds the same source and checks discovery, calls, parity and invalid arguments. Windows notebook subprocess handling is tested.

After Run All, `ask(email)` displays the verdict, source quote, retrieved examples, indicators and trace. Use a fresh thread and `review(thread_id, 'approve')` or `review(thread_id, 'reject')` for a pending quarantine. A completed thread cannot be reused. The saved demo includes a success and an actual failure.

## Validation and packaging

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe scripts\verify_saved_submission.py
.venv\Scripts\python.exe scripts\summarize_human_ratings.py
```

The saved-artifact verifier checks model-code lineage, displayed classification tables, raw prediction arithmetic, attack denominators and the exact 30-review snapshot. It does not claim a fresh model run. Full execution is available with `scripts/verify_submission_notebook.py --device cpu --mode full --reuse-assets . --allow-downloads --save-executed` or on a suitable CUDA runtime.

`scripts/prepare_submission_notebook.py` preserves saved outputs when repackaging equivalent code. It clears them if helper/pin behavior changes, or when `--clear-outputs` is requested. A prepared copy never overwrites the canonical notebook automatically.

The notebook retains an accurate assistance disclosure for code/analysis. Human-based reviews are separately recorded as the owner's work. The supplied P13 brief is covered; the separate judging document and live team rehearsal cannot be certified from this checkout.
