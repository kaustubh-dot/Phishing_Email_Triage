# Submission evidence

The canonical [notebook](../../Phishing_Email_Triage.ipynb) preserves the supplied complete 300-email GPU run and reports **30 completed human-based reviews** bound to its saved cases.

| Evidence | Scope |
| --- | --- |
| [Supplied-run record](verification/supplied-saved-run/verification.json) | Source file hash, 21 executed cells, no saved errors, 194.9 seconds on RTX 4000 Ada; post-execution edits identified. |
| [Artifact verification](verification/supplied-saved-run/artifact_checks.json) | Saved tables, unchanged model-code hashes, recomputed metrics and exact review snapshot. |
| [Source provenance](source_provenance.json) | Current and historical hashes; immutable asset revision and editing scope. |
| [Review records](../../artifacts/human_based_reviews.csv) | 30 completed human-based reviews, personally completed by the owner. |
| [Human-rating summary](../../artifacts/results/full/human_rating_summary.json) | Historical numeric means and separately verified current review completion. |
| [CPU training check](verification/cpu_training_smoke.json) | One real optimizer update, adapter save/reload and unchanged benchmark weights. |
| [Local checks](verification/local_checks.json) | Regression, dependency and presentation checks with their actual scope. |

Earlier `full`, `quick`, source-diff and CPU-partial records describe their own historical sources. They are retained as evidence, not relabelled as final target-device runs. Complete laptop/T4 timing is not certified. See [the final review](../../docs/FINAL_SUBMISSION_REVIEW.md).
