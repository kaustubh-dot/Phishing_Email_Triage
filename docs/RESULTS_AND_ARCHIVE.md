# Results and archive guide

The canonical notebook contains the implementation, evaluation code and demo. Its outputs are cleared pending a complete run of the revised explanation guards and Windows fixes.

## GPU reference results

[artifacts/results/full](../artifacts/results/full/) retains the earlier fixed 300-email GPU evaluation. Ten conditions share identical test identities. Original rank-8 has 3 false positives/4 false negatives; the full defended workflow has 13/3. The original 30-attack regression and 150-pair fresh holdout retain all outcomes, eligibility and common-pair denominators. These measurements predate the new copy/word-budget explanation guards.

The immutable [GPU archive](../archive/gpu-reference-2026-11-11/README.md) preserves the result files, two execution records and checksums from before the compatibility changes. Historical full and quick execution completed in 203.43 and 81.16 seconds on RTX 4000 Ada. The source hashes identify their exact scope.

## Local CPU checks

[Partial CPU evidence](../output/submission/verification/laptop-cpu-partial/verification.json) records 14 completed code cells through validation explanation comparison. Seven baseline rows were independently checked on 300 emails; the rank-8 CPU result differs from GPU on one email. The full-system generation was stopped for runtime, so this is not a completed full evaluation.

[CPU training evidence](../output/submission/verification/cpu_training_smoke.json) verifies one optimizer step on eight training emails, a real LoRA update and adapter save/reload in 92.84 seconds. Benchmark adapters were unchanged. Full training was not repeated.

[Local checks](../output/submission/verification/local_checks.json) record 34 passing regression tests, clean dependencies and presentation package/layout checks. No native presentation visual render was available.

## Human ratings and presentation

[Thirty completed human ratings](../artifacts/human_explanation_ratings.csv) cover the original explanation text, with counts/means/checksum in [the summary](../artifacts/results/full/human_rating_summary.json). The project owner has separately confirmed personally completing all **30/30 human reviews** of the submitted explanation cases; see [the confirmation](../artifacts/human_review_confirmation.json). The new confirmation supplies no numeric means. See [the review record guide](HUMAN_REVIEW.md).

The [presentation](../output/presentations/P13_Phishing_Triage_Updated.pptx) labels numerical measurements as GPU references. Demo slides and speaker notes follow live notebook selection; the [runbook](../output/presentations/TEN_MINUTE_RUNBOOK.md) plans the ten-minute talk and five-minute Q&A.

See [submission status](../SUBMISSION_STATUS.md), [assessment](SUBMISSION_ASSESSMENT.md) and [archive index](../archive/README.md). Large caches, embeddings, intermediate checkpoints and duplicate executed notebooks are ignored. Original and defensive adapters remain under `artifacts/adapters/`.
