# Submission status

Engineering fixes are implemented on `fix/review-data-attribution`. **Evaluation readiness remains conditional on the remaining execution checks and confirmation of the separate judging guidelines.** This review is not faculty approval or a predicted grade.

## Verified changes

- **34 regression tests pass**, including a real Windows notebook-kernel MCP launch, command-line MCP integration, explanation-copy/word-budget guards, safe rating entry and completed-rating acceptance.
- The isolated Python 3.12 environment passes `pip check`. Windows and Linux commands use the correct interpreter paths.
- The CPU training check completed one optimizer step on eight downloaded training emails, observed a LoRA update, saved/reloaded the adapter and left benchmark adapters unchanged. It took 92.84 seconds; full retraining was not repeated.
- A partial CPU notebook run completed 14 code cells through validation explanation comparison. Seven baseline rows on all 300 test emails were independently recomputed. Rank-8 CPU inference differs from the GPU reference on one email. The full-system run was stopped during slow explanation generation; no completed CPU full run or final timing is claimed.
- The verifier is portable, accepts genuine completed ratings, records backend differences and shuts down its kernel on failure. The packager preserves current source and can pin subsequently published rated assets.
- The presentation and speaker notes follow the live demo and label numerical tables as GPU references. Its appendix table fits above the footer. Package/layout checks pass; native PowerPoint visual rendering was unavailable.

## Saved results and human ratings

The earlier full/quick RTX 4000 Ada runs completed all 21 code cells in 203.43/81.16 seconds with caches. Their exact source hashes remain preserved; they do not validate the newly added explanation guards. The GPU reference full workflow has 13 false positives, 3 false negatives and F1 0.9316 on 300 emails. See [the archive](archive/gpu-reference-2026-11-11/README.md).

**30/30 human reviews are complete, personally completed by the project owner.** The owner confirmed this for the submitted explanation snapshot. See [the completion record](artifacts/human_review_confirmation.json) and [latest correction](docs/LATEST_SUBMISSION_REVIEW.md). Historical numeric scores retain their original scope; individual numeric scores were not supplied with the new confirmation.

## Remaining evaluation steps

1. Complete Run All of the final notebook on the presentation machine or permitted free Colab T4. Full mode evaluates 300 fixed emails; quick mode evaluates 60. CPU generation can take several hours. Outputs are cleared to avoid presenting earlier explanations as newly verified outputs.
2. Retain the owner-confirmed 30-review completion record with the submitted snapshot. Any subsequently entered numeric scores must describe the actual reviewed cases.
3. Confirm the professor's separate **Group Project Guidelines & Judging** document. The supplied four-page brief names it but supplies no numerical marking weights.
4. Review contributions and rehearse the ten-minute talk plus five-minute Q&A using fresh approval threads.

## Deliverables and evidence

- [Canonical notebook](Phishing_Email_Triage.ipynb), [requirements](requirements.txt) and [detailed assessment](docs/SUBMISSION_ASSESSMENT.md).
- [Presentation](output/presentations/P13_Phishing_Triage_Updated.pptx), [script](output/presentations/P13_Phishing_Triage_Full_Presentation_Script.md) and [timed runbook](output/presentations/TEN_MINUTE_RUNBOOK.md).
- [Partial CPU execution](output/submission/verification/laptop-cpu-partial/verification.json), [CPU training check](output/submission/verification/cpu_training_smoke.json), [local checks](output/submission/verification/local_checks.json) and [source provenance](output/submission/source_provenance.json).

No thresholds or benchmark adapters were changed in response to test outcomes. Classification errors, ambiguous labels, bounded-input overlap, successful attacks and simulated quarantine remain disclosed.
