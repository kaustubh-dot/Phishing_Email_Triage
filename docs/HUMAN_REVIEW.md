# Human-based review records

**30 human-based reviews are complete**, personally performed by the project owner. [human_based_reviews.csv](../artifacts/human_based_reviews.csv) contains the exact email IDs, email text, verdicts, reasons, quotes, fallback flags, reviewer and completed status. [The confirmation](../artifacts/human_review_confirmation.json) records the owner's statement and snapshot hash.

`load_human_reviews` validates all immutable fields, distinct identities, reviewer names, completed statuses and the confirmation count. It allows reordered rows and Windows line endings. Changed explanation text cannot inherit a completed review.

These records represent owner-confirmed human review completion. They are separate from automatic quote checks and per-dimension numeric scores. The original numeric rating sheet and its means remain attached to the original text. The completion confirmation supplies no new numeric means.

If the already completed reviews have numeric scores/comments in a separate file, preserve those actual judgments and enter them against the matching snapshot. The entry utility edits only score/name/comment fields and preserves other reviewers' work:

```powershell
.venv\Scripts\python.exe scripts\review_explanations.py --sheet artifacts\human_explanation_ratings_9b10d09848942b57.csv --rater "Actual reviewer name" --start 1 --end 30
```

The numeric dimensions are correctness, grounding and usefulness, each 1-5. Numeric summaries are calculated only from real entries; completion is not converted to scores. A new model/backend snapshot receives its own identity.

The standalone notebook downloads the completed case records from its immutable asset revision and embeds the same validation code. Repackaging equivalent code preserves saved outputs; changing helpers or asset pins clears them unless the updated results are separately regenerated. Use `--clear-outputs` for an explicitly fresh execution copy.
