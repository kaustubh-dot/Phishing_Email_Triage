# Evaluation readiness assessment

Reviewed against all four pages of the supplied P13 Phishing Email Triage brief. **The technical components are implemented; final execution and human validation remain required.** The separate Group Project Guidelines & Judging document was not supplied, so numerical weights and a final grade are not asserted.

| Requirement in the brief | Evidence and status |
| --- | --- |
| One self-contained notebook | Implemented; embedded helpers/dependency pins and checksum-verified runtime assets. Revised outputs are cleared pending Run All. |
| Required downloaded dataset and fixed stratified subsets | Implemented; seed 42, 4,000/400/300 identities, class-balance inspection and disjoint train/validation/test IDs. |
| Qwen LoRA, zero-shot and training-only MiniLM/FAISS retrieval | Implemented; rank-4/rank-8 adapters, masked loss, saved/reloaded weights and validation-only k selection. |
| Keyword baseline and combined comparison/ablations | Ten conditions on one fixed 300-email GPU reference subset, requested phishing-positive metrics and a common 299-email overlap sensitivity table. CPU baseline rows separately measured. |
| LangGraph roles and tools | Implemented; classifier, extractor, explainer, responder and deterministic supervisor with trace and evidence. |
| Analyst interrupt before quarantine | Approval/rejection, malformed decisions, replay and thread reuse tested. Quarantine is simulated. |
| Thirty prompt-injection variants and defence comparison | Complete GPU reference evidence, with control/attacked outcomes, eligible denominators and common-pair comparisons, plus a separate frozen holdout. The original variants share ten base scenarios. |
| At least ten analysed failures | Case-specific notes, failed conditions, labels, evidence and validation follow-ups retained. |
| Lab adaptations/references | Documented in relevant sections. The brief does not require every optional technique in each lab. |
| Laptop CPU or free Colab T4 | CPU training/save/reload passes a one-step check; partial CPU inference completes baseline and validation stages. Full CPU execution is incomplete, and T4 has not been measured. Complete this hardware requirement before evaluation. |
| Thirty human explanation ratings | Thirty completed ratings cover the original text. The revised explanation snapshot requires its own actual ratings. |
| Ten-minute talk and five-minute Q&A | Deck, script and timed runbook prepared; live rehearsal and team understanding remain human tasks. |
| MCP stretch goal | Actual stdio discovery/calls/parity/error handling passes inside a Windows notebook and subprocess tests. |

## Fixes and checks

The notebook MCP launch now uses a subprocess-capable worker event loop on Windows and a real stderr file. An actual notebook-kernel regression reproduces that path. The execution verifier uses the active interpreter, handles Windows paths without symlinks, compares CSV values across line endings, records backend prediction differences and accepts completed rating sheets.

The explainer now requests evidence supporting or conflicting with the verdict. Pure source copying and reasons above the declared 30-word limit produce visible fallbacks. These checks do not establish improved human-rated quality. The rating-entry tool preserves exact case text and other reviewers' work, and the packager updates current source without replaying historical patches.

All 34 regression tests and the isolated dependency check pass. A real CPU optimizer step updated LoRA parameters and saved/reloaded successfully in 92.84 seconds without modifying benchmark adapters. The partial CPU run completed 14 code cells through validation explanation comparison. Seven baseline rows were independently recomputed for 300 emails; rank-8 differs from the GPU reference on one email. Slow full-system generation was stopped, so no final CPU runtime or full-run success is reported.

Earlier GPU full/quick evidence remains archived with its source hashes. It does not validate the new explanation guards. The revised canonical notebook has cleared outputs to avoid mixing these snapshots. No experimental quantization was adopted.

Presentation text and speaker notes now follow actual notebook demo selection, use fresh approval threads, and label saved numerical results as GPU references. Package/layout checks pass. Native PowerPoint visual rendering was unavailable and is still advisable before presenting.

## Remaining evaluation work

1. Complete the revised notebook on the actual presentation backend or free Colab T4 and retain its outputs.
2. Enter 30 actual ratings for that run's exact explanation sheet using [the human-review guide](HUMAN_REVIEW.md). Historical scores cannot be transferred.
3. Confirm the separate judging guidelines. The supplied brief contains no numerical grading weights.
4. Review team contributions, inspect the deck in PowerPoint and rehearse the timed demo/Q&A.

The GPU reference workflow has 13 false positives and 3 false negatives. Some attacks remain successful. Quoting, automated checks and implementation coverage cannot certify useful reasoning or a final grade. See [submission status](../SUBMISSION_STATUS.md) and [the evidence guide](RESULTS_AND_ARCHIVE.md).
