# Project orientation

The canonical deliverable is `Phishing_Email_Triage.ipynb`. It preserves the owner's supplied executed 300-email GPU run. `docs/FINAL_SUBMISSION_REVIEW.md` and `output/submission/verification/supplied-saved-run/` identify the exact model-code lineage and the later portability/reporting edits.

## Human-based review evidence

The owner confirmed personally completing 30 human-based reviews. The actual case records are `artifacts/human_based_reviews.csv`; their confirmation and snapshot hash are in `artifacts/human_review_confirmation.json`. `submission_support.load_human_reviews` validates completion against the exact email/verdict/reason/quote/fallback fields. Future generated text does not inherit the reviews.

Review completion and numeric scores are separate evidence. Preserve the original numeric CSVs, reviewers and scope. Calculate means only from actual score entries. Do not create per-case scores or copy historical scores onto different explanations.

## Validation

Run the regression suite and `scripts/verify_saved_submission.py` after changes. Repackaging equivalent code preserves saved outputs; changed helper/pin behavior clears them. Any change to protected model logic requires new execution evidence. Keep source, runtime, device and cache claims tied to actual records. Complete laptop/T4 timing remains unverified.
