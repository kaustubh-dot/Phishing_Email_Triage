# Submission-testing review

Reviewer: GPT-6.1-sol, reasoning effort xhigh, independent subagent.

Baseline: published commit `821de23072bd435acc7983a2d183729fa6ffc9a4`. Scope is the bounded rating-snapshot portability correction, completed testing evidence and readiness assessment against the two supplied PDFs. This review does not retrain models, alter experiments or certify an unmeasured platform.

Result: **PASS. The notebook and follow-up documents are released for the follow-up commit/push.** Automated implementation and this testing checkpoint pass. The academic submission remains incomplete: genuine human ratings are **0/30**, contributions are placeholders, rehearsal/Q&A remain team work, and the specified laptop CPU/free Colab T4 timing is unverified.

## Finding and correction reviewed

The real FP32 desktop CPU probe generated a different reason for one of two existing cases. The published rating cell rejected the different explanation snapshot, stopping an otherwise valid rerun. The correction preserves existing sheets and scores, selects a separate fingerprinted sheet with blank human fields when the canonical sheet describes different immutable text, and counts only scores belonging to the current email/explanation snapshot. Matching rows are compared by case identity rather than file order. The summary now records the actual sheet path.

Only notebook sources `p13-021` (description), `p13-022` (rating cell) and `p13-030` (summary path) differ from the published baseline. No executable correction was necessary during independent review. Model weights, prompts, thresholds, data/splits and injection payloads remain unchanged.

## Independent checks

- Validated notebook format and Python syntax. All 17 code cells have consecutive saved full-run execution counts and no error outputs. The notebook retains its complete sections and runtime implementation; no authoring script is a runtime dependency.
- Executed the actual rating-cell source against temporary synthetic fixtures. Verified blank first creation; preservation of existing scores; acceptance of reordered rows; a different explanation selecting a distinct blank sheet; no score transfer; repeat selection of that snapshot; rejection of altered immutable text, missing required columns and duplicate case identities in the selected fingerprinted sheet; and separate quick/full paths. Synthetic scores existed only inside a deleted temporary directory, never in genuine project artifacts.
- Verified that a nonmatching canonical legacy sheet is preserved and isolated. The code cannot authenticate why that legacy text differs. Its scores are not applied to the current snapshot. Rejection of edits is guaranteed for an existing selected fingerprinted sheet; the documentation now states this boundary precisely.
- Independently recomputed every classification metric from both prediction tables: 60 quick and 300 full emails. Full-system predictions still equal rank 8, with full confusion matrix `[[185, 3], [4, 108]]` and F1 0.9686099. Summary paths select the genuine sheets; every actual rater/score/comment field remains blank, and sheet case IDs match the corresponding first 30 prediction IDs. All saved approval checks pass, with an empty final simulated quarantine log.
- Compared protected artifacts byte for byte with `821de23`: both adapters, fixed split manifest, model/data revisions, injection cases/detail, original template, both PDFs and both genuine human-rating sheets are unchanged.
- Inspected the separately executed fresh clone's saved notebook: all 17 code cells succeeded, and its complete 300-row prediction table equals the current table. The recorded 291.6-second run used a separate environment and an initially empty model/data cache, while package installation reused the existing uv wheel cache. This supports checkout reproducibility without claiming a cold package-download timing.
- Inspected the before/after real CPU probe artifacts: two cases, CPU FP32, one changed reason, both quarantine proposals paused, and zero actions executed. The recorded after-fix probe is 33.55 seconds. It is a targeted desktop compatibility check, not a full CPU benchmark or laptop measurement.
- Inspected the post-correction real GPU runs and acceptance evidence. Fresh-kernel quick/full runner times are 50.9/151.5 seconds, including startup and installation; notebook after-setup summaries are 47.19/147.93 seconds. No new model run or training was performed during this independent review. Existing real-model evidence and targeted rating fixtures cover the bounded change.

Independent check results are saved in `artifacts/submission_checks/independent_review.json`. Earlier acceptance/control checks remain separately labelled implementation evidence in `acceptance_checks.json`; they are not relabelled as this independent review. Browser evidence applies to the published `821de23` preview, not to an unpushed follow-up commit.

## Direct documentation corrections

- Replaced stale statements that fresh-checkout checks or independent review were still to follow with the completed outcomes.
- Made the readiness table use current post-correction GPU timings and distinguish them from the historical Phase 6 measurements.
- Clarified legacy-sheet isolation versus selected-fingerprinted-sheet edit rejection. No claim of rating-sheet authentication or human correctness follows from the identity check.
- Clarified that a desktop CPU compatibility probe has been timed while the full laptop CPU/Colab T4 requirement remains pending. Updated README and ROADMAP with the passed follow-up checkpoint and its limits.

## Readiness conclusion

The requirement mapping follows the supplied PDFs and keeps mandatory unfinished work visible. The brief does not set a minimum F1 or require a favourable defence result. The negative common-pair injection result, 158/300 explanation fallbacks, one bounded-input overlap and limitations of a single fixed split remain disclosed. The written human-hours estimates are planning allowances, not measured completion times or a grade prediction.

Before final university submission, the team must supply 30 genuine ratings and saved human metrics, record actual contributions, prepare/rehearse the talk and individual Q&A, complete the specified platform verification, and freeze a successful notebook with the grader's artifact-access mechanism confirmed. The available Ubuntu desktop GPU is suitable development evidence; this review neither demands new hardware nor treats the exact portability requirement as waived.

**Released for the bounded follow-up publication. No known executable defect remains within this review scope.**
