# Final submission package

The canonical [notebook](Phishing_Email_Triage.ipynb) now contains the owner's supplied complete saved execution and **30 completed human-based reviews**, with case-level review records and matching source text. Submit this file or the `fix/review-data-attribution` branch.

| Item | Status |
| --- | --- |
| Complete saved notebook | 21 executed code cells, 300 test emails, no saved error outputs. |
| Saved model behavior | Matches the supplied executed classifier, retrieval, explainer and security logic; checked by AST hashes. |
| Human-based reviews | 30 complete, personally completed by the project owner; exact case snapshot verified. |
| Human numeric means | Historical original-text means retained separately; no numeric scores invented or transferred. |
| Baselines and ablations | Ten conditions on the identical fixed subset; rank/k and defence comparisons. |
| Security and approval | Controls, attacked outcomes, common denominators, MCP parity and explicit analyst gating retained. |
| Failure analysis | At least ten detailed cases; incorrect spaced-URL claim corrected. |
| Portability | Self-contained pinned bootstrap, Windows MCP handling and safe repackaging checked separately. |
| Presentation | Saved-result deck, ten-minute spoken script, timed runbook and extended Q&A material. |

The supplied run took **194.9 seconds**, excluding dependency installation, on **NVIDIA RTX 4000 Ada** with caches and saved adapters. It reports 223 accepted model explanations and 77 visible fallbacks. The final reporting cells were refreshed from the actual owner-confirmed review records; the model was not rerun during this assembly.

Complete laptop CPU/free Colab T4 timing remains unverified. The repository includes a real one-step CPU training/save/reload check and earlier partial CPU evidence. Run the final notebook on the actual target before asserting a target-device time limit. The separate Group Project Guidelines & Judging document was not available in this checkout; no numerical grade or faculty approval is asserted.

**Final checks:** 40/40 regression tests pass; dependencies are consistent; the clean standalone bootstrap verifies all 17 immutable assets and the exact 30 human-based review records. Saved table arithmetic and model-code lineage checks pass.

Evidence: [saved-run verification](output/submission/verification/supplied-saved-run/verification.json), [artifact checks](output/submission/verification/supplied-saved-run/artifact_checks.json), [review records](artifacts/human_based_reviews.csv), [review confirmation](artifacts/human_review_confirmation.json), [source provenance](output/submission/source_provenance.json) and [final review](docs/FINAL_SUBMISSION_REVIEW.md).

The default `main` branch remains an earlier version. Use the exact final branch or notebook for evaluation. Rehearse the live demo with fresh approval threads and retain the model's actual limitations in the talk.
