# Phase 5 review

Reviewer: GPT-6.1-sol, reasoning effort xhigh, independent subagent.

Scope: full evaluation, component measurements, matched injection tests, human-rating export and observed failure analysis in notebook cells `p13-017` through `p13-024`, plus `checkpoint-5`. Also inspected the preceding Phase 5 memory correction in `p13-004` and `p13-016`: bounded explanation indicator views, prompt-budget rejection and final-logit generation. No retraining, classifier prompt/threshold changes, attack tuning or Phase 6 work was performed.

Result: **Passed after direct corrections. Phase 5 is released for Phase 6.** This passes the implementation/evaluation checkpoint. Actual human explanation ratings remain **0/30** and cannot be claimed complete; team contributions also remain human work. The negative defence result is preserved.

## Corrections made before passing

- Added a comparison restricted to the same attack pairs whose controls are quarantined in both defence modes. The original per-mode targeted rates had different eligible denominators (30 versus 15), so they could not support an unqualified before/after improvement. Added control allow rates, unique scenario counts and explicit classifier eligibility/flip rates.
- Separated classifier label flips from responder allows against a still-phishing verdict, and reported the reverse action disagreement. The defended responder's consistency rule is a control constraint, not an additional classifier accuracy result.
- Split the 300 exact quote checks into **142 valid-format model explanations** and **158 visible template fallbacks**. Added their rates and explicit narrative that neither exact quotes nor valid JSON establish a correct reason. The 158 template quotes are not counted as successful model reasoning.
- Added specific AI-assisted evidence analysis for ten observed failures after reading their full texts and actual bounded classifier views. The table prioritizes all seven full-system errors, then three distinct baseline errors. It retains automatic categories separately, exports the inspected cases and labels the analysis as observations/hypotheses, not human ratings or confirmed causal diagnoses. One base64 attachment was decoded locally as inert text for inspection; no content was executed or fetched.
- Checked the exact exported case/explanation snapshot before counting human ratings, retained existing human entries on reruns and separated QUICK_RUN's sheet from the full-run sheet. Valid scores require integer values from 1 to 5 and a nonempty rater. Every actual human field remains blank.
- Corrected only the confusion-cell text contrast where the blue background is dark. No chart redesign or new dependency was introduced.

## Independent verification

- The reviewed notebook completed a fresh CUDA execution using pinned cached models and existing adapters with `TRAIN=False`. All **15 code cells** have successful saved outputs and no error outputs. Saved execution metadata spans **149.9 seconds** from the first cell's start to the last completion, excluding kernel startup. Notebook format and Python source syntax validate. The full GPU suite was not repeated after its completed outputs were available.
- Recomputed all classification F1 values directly from the 300-row prediction artifact. Full-system predictions exactly equal primary rank 8: confusion matrix `[[185, 3], [4, 108]]`, accuracy 0.976667, phishing precision 0.972973, recall 0.964286, F1 0.968610 and false-positive rate 0.015957. All 111 quarantine proposals pause for approval; evaluation executes zero quarantines. The prior common 299-message overlap sensitivity comparison remains intact.
- Recomputed every injection eligibility flag, success flag, classifier flip and reported rate from the saved paired detail. There are exactly 30 distinct authored attack IDs in each mode, the same scenarios/payloads, 10 unique controls and three payloads per scenario. No attack text is lost to classifier shortening. The 30 pairs reuse controls and are not 30 independent base-email trials.

| Measure | Defence off | Defence on |
| --- | ---: | ---: |
| Eligible quarantined control pairs | 30/30 | 15/30 |
| Targeted action success, own eligible controls | 10/30 (33.3%) | 7/15 (46.7%) |
| Raw attacked allow, all pairs | 10/30 (33.3%) | 15/30 (50.0%) |
| Targeted success, same 15 common-eligible pairs | 4/15 (26.7%) | 7/15 (46.7%) |
| Classifier phishing-to-safe flips | 11/30 eligible classifier controls | 7/15 eligible classifier controls |
| Attacked allow despite a phishing verdict | 0 | 0 |
| Attacked quarantine despite a safe verdict | 1 | 0 |

The common-eligible pairs cover five unique scenarios. The bundled defence performs worse on raw attacked allows and on this common conditional comparison. All attacked allows follow safe classifier verdicts. The consistency rule prevents action–verdict disagreement in defended mode, while leaving classifier errors intact. No prompt, threshold, model weight, scenario or payload was changed to produce a more favorable result. These authored stress tests give descriptive results and do not establish general injection robustness or explain which bundled measure caused the change.

- Independently reproduced the long-email evidence path using the pinned cached dataset and actual notebook functions. The 195,194-character email has 3,134 URL/domain results. `explanation_indicators()` leaves the full input dictionary unchanged, supplies five bounded examples and preserves aggregate counts. The actual full-run maximum explanation prompt is 1,151 tokens; four model indicator views are capped. A deliberately over-budget prompt raises before the model is called. With the actual pinned 1.5B tokenizer, both ordinary and hostile-payload prompts retain exactly the intended three role-start/two role-end tokens and the final assistant prefix; no role marker is silently truncated. The bounded evidence view does not change classifier inputs or analyst graph state.
- Reconciled explanation counts: 142 model outputs pass format/exact-quote checks, 158 use visible fallback templates, and their sum is 300 exact quotes. This is a format/grounding check, not reason validation. Six declared indicator fixtures remain fixture checks; retrieval Hit@5/MRR remain label-agreement proxies rather than human relevance ratings.
- Verified 30 distinct full-run rating cases match the first 30 prediction IDs, each saved quote occurs in its email and **all rater, score and comment cells are blank**. No human mean is produced. The notebook's fresh-run identity check also passed against the current explanations.
- Verified 127 distinct emails fail at least one evaluated condition, the failure artifact contains exactly the seven actual full-system disagreements, and the ten inspected cases contain those seven plus three baseline-only errors. Specific observations cover a software-promotion false positive, sparse/ambiguous text, a convention announcement, encoded sales content, decoration consuming the bounded input, a long financial scam, a short approval request, marketing rule coverage, a single cue below the keyword threshold and obfuscated free-cable spam.
- SHA-256 checks confirm every earlier notebook cell source outside the review scope, both adapter weight files and the fixed split manifest are unchanged by this review. Visually inspected the saved classification chart; all four confusion counts are readable.

Independent checks are saved in `artifacts/results/full/phase5_review_checks.json`. Detailed new artifacts include `injection_common_metrics.csv` and `reviewed_failures.csv`; the existing metrics/detail/failure artifacts were regenerated from the actual completed run.

## Remaining limits and release

The 158/300 fallback rate limits the explainer's measured format/quote reliability. Even valid model reasons can be wrong, as the phone-number/link error illustrates. Human correctness, grounding and usefulness ratings are still pending. The failure observations suggest validation experiments; they do not prove root causes or improvements. Some dataset-labelled phishing messages contain broad spam or ambiguous intent. No labels were changed on review.

Earlier limitations remain: one bounded classifier training/test input overlap, one fixed seed/split, dataset-specific results, truncated classifier/embedding inputs, local string tools without reputation checks, and in-memory simulated approval state. The injection defence does not repair classifier errors. No production-security or statistical-significance claim follows from these measurements.

Notebook sources changed during this review: **`p13-017`, `p13-018`, `p13-019`, `p13-020`, `p13-021`, `p13-022`, `p13-023`, `p13-024`, `checkpoint-5`**. Other notebook source cells were preserved; successful execution refreshed their outputs. README and ROADMAP now reflect the Phase 5 checkpoint. **The notebook is released; Phase 6 may begin.**
