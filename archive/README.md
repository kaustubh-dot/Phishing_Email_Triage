# Experiment archive

This directory preserves supporting evidence and explains which implementation it describes. The active saved submission is [Phishing_Email_Triage.ipynb](../Phishing_Email_Triage.ipynb), with the owner's complete supplied GPU outputs and [30 completed human-based review records](../artifacts/human_based_reviews.csv). Its execution lineage is under [output/submission](../output/submission/). Archived measurements retain their original source, device and numeric-rating scope.

The [saved GPU reference](gpu-reference-2026-11-11/README.md) preserves the complete prior 300-email evaluation and execution records with per-file checksums. Presentation reference tables retain this snapshot; live examples follow the current notebook.

| Evidence | Scope | How to interpret it |
| --- | --- | --- |
| [Pre-review quick run](quick-run-2026-11-05/) | 60-email fixed quick subset, selected defensive checkpoint, 78.55 seconds after setup on RTX 4000 Ada | A cached historical run, not the full 300-email benchmark or the new one-file setup test. File hashes and local-source provenance are recorded in its manifest. |
| [Legacy CPU probe](legacy-cpu-probe.json) | Two examples on CPU, before the later MCP/defence changes | Tests an earlier rating-snapshot correction and CPU compatibility only. Its 33.55-second timing does not establish current full CPU/laptop/T4 runtime. The exact source commit, source path and original file hash are retained. |
| [Injection-development audit](../artifacts/results/injection_audit/) | Original adapters and fixed development cases | Diagnostic evidence motivating the current defence. The [audit report](../INJECTION_DEFENCE_REVIEW.md) predates adversarial LoRA training. |
| [Historical human ratings](../artifacts/human_explanation_ratings.csv) | 30 rated explanations from the original snapshot | Describes those exact old reasons/quotes/verdicts. None of the 30 current reasons is identical; these ratings must not be presented as evaluation of the revised explanations. |
| [GPU reference rating sheet](../artifacts/human_explanation_ratings_9b10d09848942b57.csv) | Earlier GPU full-run explanation snapshot | Contains blank human fields. The final run may create a different fingerprinted sheet; use the exact path it prints. |
| [Latest partial CPU run](../output/submission/verification/laptop-cpu-partial/verification.json) | Baselines on 300 emails and validation explanations; full-system generation incomplete | Contains no completed full CPU evaluation or injection result. One rank-8 prediction differs from the GPU reference. |

The raw quick-run JSON retains its original workspace-relative paths. This archive contains a compact metrics/prediction subset, not all email bodies, rating sheets or intermediate run files. Those paths describe the historical run and should not be interpreted as files newly produced by the reviewed notebook.

Earlier published notebook/results are also recoverable from Git history:

- [Original completed submission snapshot, before MCP and defence changes](https://github.com/kaustubh-dot/Phishing_Email_Triage/tree/864bea5).
- [MCP and explanation/retrieval revision](https://github.com/kaustubh-dot/Phishing_Email_Triage/tree/a6b6737).
- [Defensive training revision used by the completed presentation](https://github.com/kaustubh-dot/Phishing_Email_Triage/tree/955885c).
- [Published repository before this submission review](https://github.com/kaustubh-dot/Phishing_Email_Triage/tree/044821a93fc84c4b1165caea57ca8c7f63bfb414).

Model downloads, rebuildable embeddings, temporary checkpoints, local environments and duplicate executed copies are omitted from the archive. The three final adapters, model/data revisions, training metadata and frozen fixtures already have documented locations in the repository. Course-supplied PDFs are referenced by the assessment but are not republished here.
