# Results and archive guide

The notebook is the graded deliverable. Repository material supplies reproducible saved weights, detailed measurements, supporting experiments and the completed presentation; it does not replace required notebook sections or human ratings.

## Active published results

[artifacts/results/full](../artifacts/results/full/) contains the fixed 300-email evaluation of the defensively trained workflow. The combined [classification table](../artifacts/results/full/classification_metrics.csv) and [predictions](../artifacts/results/full/predictions.csv) use identical test identities across the ten conditions. The original rank-8 classifier has 3 false positives and 4 false negatives; the full defended workflow has 13 false positives and 3 false negatives.

The [original injection regression](../artifacts/results/full/injection_metrics.csv) uses 30 pairs over 10 authored malicious scenarios. The [fresh attack holdout](../artifacts/results/full/security_holdout_metrics.csv) has 150 pairs across five subsets, including benign allow-directed negative controls. The [frozen selection record](../artifacts/adapters/defended-r8/training_metadata.json) identifies the training inputs and checkpoint; the holdout was excluded from selection. Pair counts are not independent campaign counts.

The [component metrics](../artifacts/results/full/component_metrics.json), [approval checks](../artifacts/results/full/approval_checks.json), [MCP checks](../artifacts/results/full/mcp_checks.json), [overlap audit](../artifacts/results/full/classifier_input_overlap.json), [299-email sensitivity table](../artifacts/results/full/classification_metrics_without_input_overlap.csv) and [reviewed failures](../artifacts/results/full/reviewed_failures.csv) describe separate aspects of performance. A verified quote is not a human judgment that a reason is correct.

## Reviewed standalone notebook

The [canonical notebook](../Phishing_Email_Triage.ipynb) is the approved reviewed version of the separately supplied submission file. It adds self-contained setup, checksum-verified asset recovery, corrected human-rating validation, explicit repository references, design explanations and clearer demo diagnostics. Classifier weights, prompts, thresholds, splits and decision policy are preserved.

Fresh [full verification](../output/submission/verification/full/verification.json) and [quick verification](../output/submission/verification/quick/verification.json) retain the execution provenance. The active full-run summaries and tables mirror the verified full run, and the canonical notebook retains all full-run outputs. Its runtime assets are pinned to published commit `044821a93fc84c4b1165caea57ca8c7f63bfb414`, so it does not fetch a moving notebook implementation.

The [assessment](SUBMISSION_ASSESSMENT.md) lists fixes, actual test evidence and unresolved academic requirements. Publication was approved on 11 November 2026. The repository publishes one canonical notebook; the local review copy is ignored by Git.

The [human-rating summary](../artifacts/results/full/human_rating_summary.json) records **30 completed human ratings** for the original explanation snapshot, including the named rater counts, mean scores and source checksum. Revised explanations await separate review; historical scores are not transferred.

## Historical evidence

See [archive/README.md](../archive/README.md) for the cached quick run, the legacy CPU compatibility probe, original human ratings and older published commit links. The [injection audit directory](../artifacts/results/injection_audit/README.md) describes the pre-hardening investigation. Historical failures and ratings are retained with their original scope instead of being silently relabelled as current outcomes.

Large local caches, intermediate Trainer checkpoints and generated embeddings are reproducible execution aids and are ignored by Git. Final adapters and their training metadata remain under [artifacts/adapters](../artifacts/adapters/).

## Presentation

The [completed presentation](../output/presentations/P13_Phishing_Triage_Updated.pptx) and [script](../output/presentations/P13_Phishing_Triage_Full_Presentation_Script.md) refer to their stated November 5 snapshot. The reviewed notebook preserves the measured classifier/security outcomes. Its demo shows additional score/fallback diagnostics and explicitly selects an illustrative successful case; this is not a new benchmark or a change to the completed presentation.
