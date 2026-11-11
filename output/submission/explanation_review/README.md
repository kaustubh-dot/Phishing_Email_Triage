# Supplementary explanation assessment

On 11 November 2026, Codex assessed both historical and current saved explanations for the same 30 emails: 60 explanations in total. **These are AI-generated judgments, not human ratings.** They are separate from the required human-rating sheet and do not count toward its completion. This was one non-blinded reviewer; the scores are subjective diagnostic judgments, not a new independent evaluation or a statistical significance result.

Every case and both snapshots are retained in [the detailed CSV](supplementary_explanation_assessment.csv). Columns use the `ai_` prefix, and each row identifies the reviewer type as `AI`. The [summary](summary.json) records paired comparisons and hashes of the source CSVs. The original human-rating files were not edited.

## Scoring criteria

Each dimension uses the same 1-5 scale for both snapshots:

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Correctness | Contradicts the email or invents a key fact | Partly accurate, incomplete or inadequately qualified | Accurate, appropriately qualified and responsive to the verdict/evidence |
| Grounding | Main claims lack source support or a matching quote | Partial support; selected quote misses relevant claims | Main claims are directly supported by the selected exact source evidence |
| Usefulness | Gibberish, misleading guidance or no usable rationale | Points to relevant context but leaves major reasoning gaps | Specific evidence, clear decision relevance and useful uncertainty/context |

Scores 2 and 4 represent intermediate judgments. Dataset-label agreement alone is not explanation correctness. A fallback is assessed as the explanation actually shown to the analyst. Exact copying can score well for grounding while remaining unhelpful. Sender claims about consent, discounts or legitimacy are not accepted as independently verified facts.

## Results

| Dimension | Historical snapshot | Current snapshot | Current higher / tied / lower |
| --- | ---: | ---: | --- |
| Correctness | 2.83 | 3.17 | 12 / 14 / 4 |
| Grounding | 2.80 | 3.67 | 16 / 12 / 2 |
| Usefulness | 1.97 | 2.37 | 11 / 16 / 3 |

The current explanations are stronger on average under this assessment, particularly in grounding. They remain limited in usefulness. The complete paired results are reported without choosing favorable rows or substituting historical human means. Historical human means reflect different reviewers and must not be compared directly with these AI-derived means.

Some improved cases remove unsupported website/link claims or identify visible product solicitations and ordinary technical correspondence. Regressions remain: the forwarded conference request is incorrectly explained as phishing, and a refinancing explanation repeats an unverified promotional promise in the sender's voice. Other accepted outputs copy noisy text rather than explain a verdict. The Red Hat false positive remains inadequately justified.

Two classifier/workflow verdicts differ between snapshots, so this comparison does not isolate the explainer method. The current classifier/security policy was already frozen; these test-case judgments are not used to retune that policy or select a more favorable benchmark. Both the old and current evidence remain archived.

To recompute the arithmetic from the recorded scores:

```bash
.venv/bin/python scripts/summarize_explanation_review.py
```

The [current human-rating sheet](../../../artifacts/human_explanation_ratings_9b10d09848942b57.csv) still has 0/30 completed genuine ratings. A person can use the cases as a worksheet but must make and record their own judgments. No team member is assigned as the author of these supplementary scores.
