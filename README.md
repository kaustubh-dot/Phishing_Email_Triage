# Phishing Email Triage — P13

See [ROADMAP.md](ROADMAP.md) for the agreed scope, phases, team and review checkpoints.

The implementation is in `Phishing_Email_Triage.ipynb`, adapted from the supplied notebook template. The original template and PDFs remain unchanged. Course labs are read from the supplied ZIPs; they are not executed blindly or committed as large archives.

## Run locally

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name python3
```

Open the notebook using `.venv/bin/python` as its Python kernel. Run the cells in order. Initial data/model downloads need internet access. GPU execution requires access to the NVIDIA device; the Codex sandbox hides it, so GPU runs here use the approved execution environment outside that sandbox.

`QUICK_RUN=True` evaluates a small fixed test sample. Setting it to `False` evaluates the full fixed comparison subset. Dataset/model revisions and split identities are recorded under `artifacts/`. Public data and model caches stay in `.cache/`.

## Current checkpoint

All six automated implementation phases are complete and have passed GPT-6.1-sol xhigh review. The canonical notebook contains the complete system, saved full-run outputs, evaluation and live demo. This is **not yet a completed academic submission**: actual contributions, 30 genuine human ratings and presentation rehearsal remain pending.

Phase 1 is complete: isolated dependencies, verified CUDA, reproducible data cleaning and splits, class-balance inspection and keyword baseline. The notebook has saved successful outputs. A GPT-6.1-sol xhigh reviewer independently reproduced the splits and baseline, then passed the checkpoint. See `reviews/phase-1.md`.

The full evaluation subset has 300 emails (188 safe, 112 phishing). The keyword baseline obtains accuracy 0.6433, phishing precision 0.7273, recall 0.0714, F1 0.1301 and false-positive rate 0.0160. These limited rules miss most dataset-labelled phishing emails. Metrics and split identities are saved in `artifacts/results/full/`.

Phase 2 is complete and has passed GPT-6.1-sol xhigh review; see `reviews/phase-2.md`. Training-only MiniLM/FAISS retrieval selects k=5 on validation data and obtains test F1 0.9511. Unchanged zero-shot Qwen predicts all 300 test emails as safe (phishing F1 0); validation scoring checks confirm this measured failure. The notebook documents its constrained next-token scoring and truncation, and saves a retrieved evidence example.

Phase 3 is complete and has passed GPT-6.1-sol xhigh review; see `reviews/phase-3.md`. Qwen LoRA ranks 8 and 4 were trained for one epoch on the same 4,000 emails and saved with pinned model revision and training metadata. The predeclared primary rank 8 obtains test F1 0.9686 (3 false positives, 4 false negatives); rank 4 obtains F1 0.9589 (2 false positives, 7 false negatives). These are fresh saved-adapter inference results. A residual Trainer autocast difference in the initial evaluation was corrected without changing weights or tuning the prompt/threshold.

One distinct safe training/test email pair becomes identical after classifier truncation. The fixed 300-message split is preserved and the limitation is explicit; a separate common 299-message sensitivity check is saved for every condition. Primary rank-8 F1 stays 0.9686; rank-4 F1 rises to 0.9633 because it misclassified that safe email. This one-seed, dataset-specific comparison does not establish a statistically significant or real-world advantage.

Phase 4 is complete and has passed GPT-6.1-sol xhigh review; see `reviews/phase-4.md`. The rendered LangGraph supervisor connects classifier, local indicator tools, explainer, responder and analyst approval. Quarantine is simulated, pauses before acting, and requires the exact `approve` decision; rejection, safe allow, replay protection and thread isolation pass. Each email uses a fresh graph thread. Checkpoints and the demonstration log are in memory and disappear when the kernel restarts.

A fresh full-subset CUDA run at the Phase 4 checkpoint completed in 30.0 seconds with all 11 then-current code cells successful. Two workflow emails provided component smoke checks. Exact quote checks and visible explanation fallbacks work, but a verified quote does not establish a correct reason: the observed model response calls a phone number a link even though the local tools find no URL. Defended actions remain constrained to the classifier verdict and separate analyst approval.

Phase 5 is complete and has passed GPT-6.1-sol xhigh review after direct corrections; see `reviews/phase-5.md`. A fresh full CUDA execution saved all 15 successful code-cell outputs (149.9 seconds from the first cell start to the last cell completion, excluding kernel startup). The full defended workflow preserves rank-8 F1 0.9686 and confusion matrix `[[185, 3], [4, 108]]`. All 111 quarantine proposals pause for approval; evaluation executes no quarantine.

Explanation checks distinguish 142 model outputs with valid format and an exact quote from 158 visible template fallbacks. All 300 quotes occur in the email, including fallback quotes; this is not a measure of reason correctness. Complete local indicators remain in graph state, while the model receives at most five bounded URL/domain examples plus counts; the largest observed explanation prompt is 1,151 tokens under a 4,096-token guard.

The 30 authored injection pairs share 10 synthetic malicious scenarios. The observed defence result is negative: raw attacked allow rates are 10/30 off and 15/30 on. Conditional targeted success is 10/30 off versus 7/15 on because eligible controls differ; on the same 15 pairs eligible in both modes, it is 4/15 versus 7/15. All attacked allow outcomes follow a safe classifier verdict; an action consistency rule cannot repair that error. These descriptive results do not establish general injection robustness.

Ten distinct failures now have specific AI-assisted evidence analysis: all seven full-system errors and three additional baseline errors. Thirty explanations are exported in `artifacts/human_explanation_ratings.csv`; genuine human ratings remain **0/30**, with every human entry blank. QUICK_RUN uses a separate rating sheet under its result directory. The export is ready for people to complete; no human quality score is claimed.

Phase 6 is complete and has passed GPT-6.1-sol xhigh review after clarifying the common injection comparison and completing primary reference links; see `reviews/phase-6.md`. Fresh-kernel runs passed in both modes: 60 emails in quick mode and 300 in full mode. The notebook's runtime summaries record 44.28 and 149.96 seconds after setup imports, excluding dependency installation. Runner wall times were 47.9 and 153.5 seconds including kernel startup and the installation cell. These cached-model, saved-adapter measurements are from the local RTX 4000 Ada GPU. CPU/Colab T4 timing remains unverified. The earlier quick environment record omits the subsequently added NumPy version field; NumPy remained at 2.5.4 and the final full record includes it.

Contributions remain to be discussed. Explanation ratings require real human input; the implementation exports the sheet and preserves existing entries on reruns.

## Notebook controls and artifacts

- `QUICK_RUN=True`: 60 fixed test emails; `False`: all 300. An explicit `P13_QUICK_RUN=1` or `0` environment setting overrides the flag; the recorded environment shows the effective value.
- `TRAIN=False`: load matching saved adapters, training once only if missing. `TRAIN=True`: retrain both ranks once. A mismatching saved adapter raises a clear error rather than being silently reused.
- `ask(email)` returns a new thread ID and prints the explanation, evidence and trace. Use `review(thread_id, 'approve')` or `review(thread_id, 'reject')` for a pending simulated quarantine. Reused or completed threads are rejected.
- `artifacts/adapters/r8/` and `r4/`: saved LoRA adapters and metadata. `artifacts/revisions.json`: pinned model/data revisions.
- `artifacts/results/full/`: the complete comparison, predictions, graph/chart, injection pairs and metrics, failure analysis and runtime summary. Quick outputs use `artifacts/results/quick/`.
- `artifacts/human_explanation_ratings.csv`: the full-run human rating sheet. Complete the rater ID and all three integer ratings (1–5) for each case, then rerun to summarize. Preserve immutable email/explanation columns; a mismatching sheet is rejected. Quick mode has its own sheet.
- `reviews/phase-1.md` through `phase-6.md`: completed independent reviews. `artifacts/results/full/phase6_review_checks.json` records the final checks.

The notebook contains the presentation walkthrough. Contributions, 30 genuine human ratings and rehearsal remain team work before academic submission. Runtime has been measured on this local GPU; CPU and Colab T4 execution have not been timed.
