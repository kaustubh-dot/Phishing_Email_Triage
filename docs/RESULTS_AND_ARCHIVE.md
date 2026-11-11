# Results and archive guide

The [canonical notebook](../Phishing_Email_Triage.ipynb) now preserves the owner's complete supplied GPU execution, with review reporting refreshed from the exact 30-case human-based review records. The supplied model behavior is preserved; setup/reporting edits are separately identified in provenance.

[artifacts/results/full](../artifacts/results/full/) contains the matching classification, security, component and human-review summaries. Every classification row uses the same 300 emails. The full workflow has 13 false positives and 3 false negatives. The saved explanation counts are 223 accepted model outputs and 77 visible fallbacks.

[Supplied-run evidence](../output/submission/verification/supplied-saved-run/verification.json) records the owner's file hash, saved 194.9-second GPU runtime, model-code hashes and the post-execution editing scope. [Artifact checks](../output/submission/verification/supplied-saved-run/artifact_checks.json) independently verify the displayed tables, raw numerical results and exact 30-review snapshot. They do not claim a new inference run.

[Human-based review records](../artifacts/human_based_reviews.csv) document 30 completed reviews personally performed by the owner. [The confirmation](../artifacts/human_review_confirmation.json) supplies the completion source and snapshot hash. Original numeric means remain in their [historical summary](../artifacts/results/full/human_rating_summary.json); no current numeric means are inferred.

The [GPU archive](../archive/gpu-reference-2026-11-11/README.md), earlier full/quick verifier runs and [partial CPU experiment](../output/submission/verification/laptop-cpu-partial/verification.json) describe their own sources and devices. The earlier CPU experiment used the experimental explanation-guard revision; it is not a completed run of this final saved-output version. Complete laptop/T4 timing remains unverified.

The [presentation](../output/presentations/P13_Phishing_Triage_Updated.pptx) uses the supplied saved GPU metrics. Use the [ten-minute script](../output/presentations/TEN_MINUTE_SCRIPT.md) for delivery and the extended script for study. Model/data caches and intermediate checkpoints are ignored; final adapters and immutable review assets are included.
