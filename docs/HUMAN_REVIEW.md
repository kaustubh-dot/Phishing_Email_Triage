# Complete the explanation review

The original explanation snapshot has 30 completed human ratings. Revised explanations need their own entries. Scores stay attached to the email, verdict, reason, quote and fallback text that was actually reviewed.

1. Run the final notebook on the presentation backend. Its human-rating cell prints the active fingerprinted CSV path. Use that exact file, including for a CPU run that produces different text from a GPU run.
2. Three people can review cases 1–10, 11–20 and 21–30, respectively. Each person must read the full email, displayed reason and quote and enter their actual name and judgments.
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
