# Human review completion and score records

**30/30 human reviews are complete. The project owner confirmed personally completing all 30 reviews of the submitted explanation cases.** See [the completion record](../artifacts/human_review_confirmation.json). Individual numeric scores were not supplied with the confirmation. Empty score cells must not be described as zero completed human reviews. Historical spreadsheet means remain attached to their original snapshot.

The instructions below describe recording individual scores or reviewing a future changed snapshot; they do not mark the confirmed reviews as outstanding.

1. Run the final notebook on the presentation backend. Its human-rating cell prints the active fingerprinted CSV path. Use that exact file, including for a CPU run that produces different text from a GPU run.
2. One person can review all 30 cases; multiple reviewers are optional. When entering numeric records, use the actual reviewer's name and judgments for the email, reason and quote.
3. Use the CSV directly, editing only `rater`, `correctness_1_to_5`, `grounding_1_to_5`, `usefulness_1_to_5` and `comment`, or use the entry tool below. The entry tool preserves case text, saves each entry atomically and refuses to overwrite an existing rating by default.

```powershell
.venv\Scripts\python.exe scripts\review_explanations.py --sheet artifacts\human_explanation_ratings_HASH.csv --rater "Actual reviewer name" --start 1 --end 10
```

On Linux/Colab, use `.venv/bin/python` or the active notebook interpreter instead. Replace `HASH` with the actual path printed by the final run.

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Correctness | Contradicts the email or invents facts | Partly accurate or incomplete | Accurate, qualified and responsive to the verdict |
| Grounding | Claims lack source support | Some claims supported; quote misses key evidence | Claims directly supported by the quoted email |
| Usefulness | Misleading, gibberish or no usable rationale | Relevant context with reasoning gaps | Explains the decision, evidence and useful uncertainty |

Scores 2 and 4 are intermediate judgments. Correct classification, a source-matching quote and a nonfallback flag do not establish explanation quality. Evaluate the reason actually shown, including template fallbacks.

After all 30 entries are complete, rerun the rating and summary cells in the same kernel, or Run All with the same backend. The loader validates the exact snapshot and calculates counts and means from actual rows. The execution verifier accepts completed ratings; it does not require a blank sheet.

If the rated assets must be downloaded by a standalone notebook, first commit and publish the rated CSV. Then package from that immutable revision:

```powershell
.venv\Scripts\python.exe scripts\prepare_submission_notebook.py --asset-revision COMMIT_SHA --ratings artifacts\human_explanation_ratings_HASH.csv
```

Check the prepared notebook in a fresh workspace before replacing the canonical submission. The packager clears saved outputs and preserves the source notebook, current classifier/security policy and original human entries. It never commits or pushes automatically.
