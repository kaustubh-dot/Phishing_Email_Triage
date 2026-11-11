# Submission verification evidence

The canonical implementation is [Phishing_Email_Triage.ipynb](../../Phishing_Email_Triage.ipynb). Its revised outputs are cleared pending Run All; historical execution records remain preserved.

| Evidence | Scope |
| --- | --- |
| [Source provenance](source_provenance.json) | Original/current hashes and explicit scope of subsequent compatibility changes. |
| [Historical source diff](source_changes.diff) and [cell hashes](preserved_system_sources.json) | Earlier reviewed implementation; not a diff for the current changes. |
| [Original rating diagnostic](original_rating_diagnostic.json) | Earlier missing-file and explanation-snapshot mismatch. |
| [GPU full](verification/full/verification.json) / [GPU quick](verification/quick/verification.json) | Earlier complete 21-cell runs, 300/60 emails, 203.43/81.16 seconds on RTX 4000 Ada. |
| [Partial CPU](verification/laptop-cpu-partial/verification.json) | Fourteen completed code cells, seven baseline rows independently checked on 300 emails, validation explanation comparison; full-system run incomplete. |
| [CPU training smoke](verification/cpu_training_smoke.json) | One actual optimizer step, LoRA update and save/reload; no full retraining. |
| [Local checks](verification/local_checks.json) | 34 regression tests, pip check and presentation package/layout checks. |
| [Original human-rating summary](../../artifacts/results/full/human_rating_summary.json) | Thirty completed ratings, names and means for the original explanation snapshot. |

Earlier GPU runs reuse packages/model/data caches and the full run downloaded/verified 15 missing repository assets. They predate the current copy/word-budget guards. CPU inference shows one rank-8 prediction difference; arithmetic is not assumed identical across devices.

No incomplete run is reported as successful and no ratings are transferred onto changed explanations. Complete Run All on a permitted backend, rate its exact 30-case sheet, and confirm the separate judging guidelines before evaluation. See [the assessment](../../docs/SUBMISSION_ASSESSMENT.md).
