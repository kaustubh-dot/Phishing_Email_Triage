# Submission notebook assessment

Reviewed on 11 November 2026 against the supplied **P13: Phishing Email Triage** brief and **Group Project Guidelines & Judging**. The presentation has already been completed; this review concentrates on the notebook, supporting evidence and reproducibility.

**State:** publication was approved on 11 November 2026. The reviewed notebook is the canonical [Phishing_Email_Triage.ipynb](../Phishing_Email_Triage.ipynb), with supporting checks and archives included. The supplied Downloads file is preserved.

## Main finding

The implementation covers the required technical system well: the specified Hugging Face dataset, keyword/zero-shot/kNN/LoRA comparisons, training-only retrieval, LangGraph specialist roles, local indicator tools, explanation generation, human approval, injection evaluation, rank/k/defence ablations, error cases and MCP stretch goal are present. The strongest issues in the supplied submission file were rating provenance and single-file execution, rather than a missing classifier or graph component.

The notebook is not yet defensibly complete for every academic requirement: 30 people-provided ratings of the current explanations are still outstanding. Full and quick execution are verified on NVIDIA RTX 4000 Ada. No additional laptop/free Colab T4 test is being pursued at the user's request; no result on those devices is claimed. Team review of the revised work remains a human responsibility. There is no reliable way to guarantee full marks from a notebook inspection or predict a particular AI evaluator's score.

## Comparison with the pre-review published notebook

The supplied file and pre-review published notebook each had 38 cells, including 21 executed code cells. Their implementation sources differed only in the human-rating cell, apart from a removed comment. The supplied file did not introduce a new model, decision threshold, split or defence policy.

- Supplied file SHA-256: `721e1714907b92cea1af7aff1598a8edb618af32c8e4f36c6863dbefdac3066c`.
- Pre-review published notebook SHA-256: `55e9f554b6c466da244a1c2640f7587b31e99f8e391e42b878537b57c8d7a931`.
- Pre-review published repository reference: `044821a93fc84c4b1165caea57ca8c7f63bfb414`.

### Issues found and corrected

| Priority | Finding in supplied notebook | Correction and evidence |
| --- | --- | --- |
| High | The rating cell creates a current fingerprinted sheet but continues reading the old canonical sheet. It can report 30/30 current ratings for different explanations. | Only a sheet matching all current case IDs, labels, verdicts, reasons, quotes and fallback flags supplies scores. Historical human work is preserved separately. |
| High | The old/current case identities match, but **all 30 reason strings and 2 verdicts differ**; selected quotes also change. Historical means therefore do not evaluate the revised workflow. | The corrected full run reports **0/30** current ratings and does not transfer the old means. [Reproduction diagnostic](../output/submission/original_rating_diagnostic.json) shows the original code counting 30 ratings despite an exact-snapshot mismatch. |
| High | With no rating sheet present, the supplied cell attempts to read a nonexistent CSV. | First execution creates a blank current sheet; reruns preserve matching entries. The original failure was reproduced as `FileNotFoundError`; the corrected path is regression-tested. |
| High | `%pip install -r requirements.txt` needs a separately supplied file, so the notebook alone fails at setup. Missing saved artifacts can also cause unnecessary retraining and moving revision resolution. | Dependency pins and all executable support are embedded. Missing saved artifacts are fetched from a fixed GitHub commit and checked against a 15-file SHA-256 manifest. Exact model/data revisions are embedded. The dataset itself is still obtained with `load_dataset`. |
| Medium | A printed statement attributes ten ratings to each team member regardless of the actual loaded rows. | Rater counts are derived only from valid rows of the matching current sheet. No names or scores are filled automatically. |
| Medium | Saved rating output reports 30/30, while the final saved summary still reports 0/30. | All 21 code cells were rerun, so saved outputs and final metadata agree. |
| Medium | Runtime previously excluded setup without a total-run figure. | The final summary includes setup, model/evaluation execution and total observed time. Cache and hardware assumptions are stated. |
| Medium | A bare notebook does not point clearly to presentation, historical results or additional evidence. | A visible repository link and supporting-results description are in the opening cell and references. Repository guides distinguish current results, historical experiments, legacy ratings and local caches. |
| Clarity | Demo output did not show the separate original/structured/plain scores or explicitly print the fallback flag. | These diagnostics are printed. The success example is chosen by an explicit post-evaluation presentation rule; this does not alter any benchmark prediction or update the completed presentation. A nonfallback quote is still not a proof of semantic explanation quality. |

## Assessment against the actual rubric

The notebook accounts for **60 marks**. Presentation accounts for 25 and Q&A for 15; those live-performance marks cannot be inferred from the file. The optional MCP stretch goal can earn up to five bonus marks, at the judges' discretion and within the overall cap.

| Notebook criterion | Marks | Evidence in the reviewed notebook | Remaining concern |
| --- | ---: | --- | --- |
| Problem and data | 8 | Clear triage question; required dataset loaded in code; filtering, deduplication, stratification, fixed seed, class balance, examples and explicit 4,000/400/300 subsets. | The dataset is spam-heavy, with ambiguous labels and campaign near-copies. One identical bounded training/test input is disclosed and a common 299-email sensitivity table is retained. |
| Required components | 22 | Three classifier approaches plus keyword baseline; PEFT training/loading with masked prompt/padding loss; MiniLM/FAISS evidence; @tool indicators; model-backed explanation and action roles; graph/checkpoint/interrupt; component and end-to-end checks. MCP stdio discovery and actual tool calls work. | Current explanation quality still needs the required 30 human ratings. Exact quote and schema checks do not establish semantic correctness. |
| Design choices and depth | 8 | Rank 4/8 and k = 1/3/5 comparisons, validation-only selection, multiple security ablations, separate baseline/defensive adapters, label-preserving adversarial training and stated simpler alternatives. | The supervisor is a fixed workflow, not autonomous planning. The notebook explains this choice without claiming an unmeasured accuracy benefit from graph orchestration. |
| Evaluation | 12 | Ten conditions on the identical fixed test subset, one combined table, chart/confusion matrix, all requested classification metrics, paired injection controls, raw errors, conditional denominators and common-pair comparisons. | Security rows have correlated authored scenarios; no broad immunity, campaign independence, statistical significance or calibrated probability is established. Human explanation evaluation is incomplete. |
| Error analysis and ethics | 5 | At least ten distinct failures with categories, source evidence, inspection scope and validation follow-ups; explicit privacy, false-positive/negative, authenticity and simulated-action limits. | Proposed fixes are hypotheses, not demonstrated gains. Review those conclusions as a team. |
| Reproducibility and clarity | 5 | Fresh full and quick Run All, all outputs saved, pinned versions/revisions, embedded helpers, first-run asset recovery, fixed seeds and configuration, independent metric recomputation and 24 tests. | Current timed runs use RTX 4000 Ada with cached packages and Hugging Face models/data. The course brief names laptop/free T4 hardware; those devices were not tested and no compatibility or runtime claim is made for them. |

The technical coverage is strong. The remaining human-rating gap and the difference between tested hardware and the course brief remain relevant to grading. The review does not assign a speculative final score or treat the completed presentation as ungraded work to redo.

## Actual verification performed

| Check | Result |
| --- | --- |
| Regression tests against the reviewed source | **24/24 pass**, including MCP subprocess integration and ten setup/rating-provenance cases. One case verifies that supplementary assessment columns cannot count as human ratings. |
| Notebook-only full Run All | **21/21 code cells**, **300 emails**, **0 error outputs**; latest recheck **203.43 seconds** including setup/kernel harness on RTX 4000 Ada. |
| First-run repository assets | No saved repository assets were prepopulated. **15 missing files were downloaded and SHA-256 verified**. Hugging Face model/data and installed-package caches were reused; this is not a cold model-download benchmark. |
| Quick Run All | **21/21 code cells**, **60 emails**, **0 error outputs**; latest recheck **81.16 seconds** including setup/kernel harness. It reused the verified artifacts and offline Hugging Face caches, with **0 asset downloads**. |
| Prediction preservation | Full and quick prediction CSVs match their published/pre-review references exactly. |
| Independent numerical checks | All ten classification rows recomputed from predictions in each mode; all 60 original off/on attack rows checked; all 900 held-out policy/case rows and 30 subset/policy summaries checked, including raw errors and common-eligible denominators. |
| Training/selection provenance | Parent adapter byte hash and canonical frozen-holdout hash match the saved training metadata. No training/test identities are mixed in the fixed manifests; focused regression checks cover augmentation labels and holdout separation. |
| Current rating sheet | Exact snapshot verified. The historical 30-row sheet is preserved. **0 current completed ratings** are reported consistently. |
| Dependency environment | Pins match the working Python 3.12 environment; `pip check` passes. NumPy 2.5.4's published Python requirement is 3.12 or newer. |
| Presentation consistency | Main classifier/security values remain unchanged. The presentation is retained as the completed historical snapshot; no new presentation is required by this review. |

Machine-readable evidence is under [verification/full](../output/submission/verification/full/) and [verification/quick](../output/submission/verification/quick/). These scripts reproduce the relevant checks:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
.venv/bin/python scripts/verify_submission_notebook.py --notebook Phishing_Email_Triage.ipynb --mode full --save-executed
```

`P13_NOTEBOOK_PATH` can select another local notebook for the policy tests; the default is the canonical root file. The optional full execution verifier requires the project virtual environment and populated Hugging Face model/data caches. Its measured checks reuse those caches; the notebook itself supports first-use downloads.

The full execution uses included adapters. The original/defensive training implementations and their recorded training/selection metadata were inspected; a complete new `TRAIN=True` retraining experiment was not repeated for this review. A no-internet first run with no models or saved assets cannot work; the notebook now gives an actionable setup error rather than silently presenting saved results as fresh inference.

## How to read the unchanged results

On the 300-email test, original rank-8 LoRA has **97.67% accuracy, 96.86% F1, 3 false positives and 4 false negatives**. The full defended workflow has **94.67% accuracy, 93.16% F1, 13 false positives and 3 false negatives**. The defence prioritizes the measured injection threat and slightly higher recall at a substantial false-positive cost. It is not an across-the-board clean-accuracy improvement.

On the original regression suite, all 30 controls are eligible in both modes: targeted success drops from **10/30 to 1/30**. On the fresh holdout, current attacked allows are **2/30** for downloaded phishing-labelled examples and **0/30** for explicitly malicious examples; benign forced-quarantine successes still occur. The historical audit and current holdout are different experiments and should not be combined into one unseen benchmark.

All 300 displayed quotes are source-verified; **223 generated explanations** pass the limited checks and **77 use visible template fallbacks**. A generated reason can still copy unhelpful text or fail to explain the verdict. This is why genuine human ratings remain necessary.

## Remaining improvements before final submission

1. **Complete the 30 current ratings.** Use [the current sheet](../artifacts/human_explanation_ratings_9b10d09848942b57.csv), scoring correctness, grounding and usefulness from 1 to 5 and recording the actual rater. Edit human fields only. Rerun with the same backend, verify the exact snapshot, and save the resulting means and count. Historical ratings cannot be carried over just because email identities are the same.
2. **Report the verified hardware accurately.** Full and quick runs completed successfully on NVIDIA RTX 4000 Ada, with no execution-error outputs. No additional laptop/free Colab T4 run is requested. Those platform results remain unmeasured, and the runtime statement is scoped to the actual tested device.
3. **Review the revised source as a team.** Confirm the contribution table and understand the LoRA objective, training-only evidence, bundled defence, fallback rates and approval boundary. The completed presentation is not being reopened.
4. **Optional future research:** study threshold calibration, false-positive costs, grouped campaign splits, uncertainty intervals and indicator/retrieval conflicts using development data, then freeze a policy and use fresh evaluation cases. These would be new experiments; the current scored test and holdout should not be reused to tune a more flattering result.

## Approved publication

The approved reviewed version replaces the repository's [Phishing_Email_Triage.ipynb](../Phishing_Email_Triage.ipynb). The support module, tests, verification evidence, archive guides and refreshed full-run metadata accompany it. One canonical notebook is published on `main`; the duplicate local review copy is ignored by Git. The original input and comparison hashes are retained in the source provenance.

If genuine ratings are completed later, publish those assets in an immutable commit and update the notebook's asset revision/manifest before finalizing it. A new grader workspace must be able to retrieve the rated snapshot, rather than download the older blank sheet while displaying completed-rating outputs from a different local workspace.

Supporting links: [results/archive guide](RESULTS_AND_ARCHIVE.md), [archive index](../archive/README.md), [source provenance](../output/submission/source_provenance.json). Dependency reference: [NumPy 2.5.4 on PyPI](https://pypi.org/project/numpy/2.5.4/).

## Supplementary explanation recheck

The supplementary assessment covers all 30 historical/current explanation pairs (60 explanations) under the same three criteria. Current versus historical means were **3.17 versus 2.83 for correctness**, **3.67 versus 2.80 for grounding**, and **2.37 versus 1.97 for usefulness**. These subjective diagnostic judgments come from a non-blinded comparison separate from the required rating sheet. All case notes, scores and regressions are retained in [the supplementary assessment](../output/submission/explanation_review/README.md).

The current snapshot improves grounding on average under this assessment, but copy-only outputs, unsupported claims and false-positive rationalizations remain. No old human mean is substituted for a current explanation, and no human name is attached to the new supplementary scores. The frozen classifier/security policy remains unchanged. The required current human-rating count remains 0/30.
