# Submission status

Verified and approved for publication on 11 November 2026.

The reviewed standalone [Phishing_Email_Triage.ipynb](Phishing_Email_Triage.ipynb) is the canonical submission notebook. It includes all saved full-run outputs and the project repository link. Supporting code, detailed checks and historical evidence are included. The current explanations still require 30 genuine human ratings and team review; the separate Codex assessment is not counted as human input.

## Submission contents

| Item | Location |
| --- | --- |
| Complete implementation, saved outputs and demo | [Phishing_Email_Triage.ipynb](Phishing_Email_Triage.ipynb) |
| Setup and running instructions | [README.md](README.md) and [requirements.txt](requirements.txt) |
| Detailed assessment and remaining requirements | [docs/SUBMISSION_ASSESSMENT.md](docs/SUBMISSION_ASSESSMENT.md) |
| Current versus historical evidence guide | [docs/RESULTS_AND_ARCHIVE.md](docs/RESULTS_AND_ARCHIVE.md) |
| Original and defensive LoRA adapters | [artifacts/adapters](artifacts/adapters/) |
| Full classification, security and component results | [artifacts/results/full](artifacts/results/full/) |
| Frozen development and held-out attack specifications | [artifacts/security](artifacts/security/) |
| Defence changes and measured tradeoffs | [DEFENCE_IMPROVEMENTS.md](DEFENCE_IMPROVEMENTS.md) |
| Historical injection audit | [INJECTION_DEFENCE_REVIEW.md](INJECTION_DEFENCE_REVIEW.md) |
| MCP indicator server | [mcp_indicator_server.py](mcp_indicator_server.py) |
| Portable setup and exact rating validation | [submission_support.py](submission_support.py) |
| Regression tests | [tests](tests/) |
| Supplementary Codex explanation assessment | [output/submission/explanation_review](output/submission/explanation_review/) |
| Archived supporting experiments | [archive/README.md](archive/README.md) |
| Completed presentation, 24 slides | [P13_Phishing_Triage_Updated.pptx](output/presentations/P13_Phishing_Triage_Updated.pptx) |
| Presentation script and viva answers | [P13_Phishing_Triage_Full_Presentation_Script.md](output/presentations/P13_Phishing_Triage_Full_Presentation_Script.md) |

## Automated verification

- All **24 regression tests** pass, including actual MCP stdio discovery, calls and invalid-argument rejection, frozen holdout separation, label-preserving augmentation, exact rating snapshots, missing-sheet creation and separation of AI score columns from human ratings. Normal subprocess access is required for the MCP integration test.
- The full notebook completed **21/21 code cells**, **300 test emails** and **0 execution-error outputs** in **203.43 seconds** including setup/kernel harness on NVIDIA RTX 4000 Ada. No repository assets were prepopulated: the notebook downloaded and SHA-256 verified all 15 missing saved files. Packages and Hugging Face model/data caches were reused.
- QUICK_RUN completed **21/21 code cells**, **60 test emails** and **0 execution-error outputs** in **81.16 seconds**, reusing verified assets and offline Hugging Face caches.
- Full and quick predictions exactly reproduce their pre-review references. Independent checks recompute all ten classification rows, all 60 original off/on attack rows and all 900 held-out policy/case rows, including the common-eligible denominators.
- The canonical notebook's source hash matches both execution records. Embedded MCP, defence and submission-support sources match the standalone files.
- `pip check` reports no broken requirements. The pinned environment is Python 3.12. First-use uncached model download time depends on the network.
- Training, validation and full test email identities are disjoint. One bounded classifier-input overlap remains disclosed with a common 299-email sensitivity table.
- The current rating snapshot is verified. All three existing human-rating CSVs are preserved. Current completed human ratings remain **0/30**.

Detailed run provenance is under [output/submission/verification](output/submission/verification/); the source/input hashes are in [source_provenance.json](output/submission/source_provenance.json).

Reproduce the regression and dependency checks from the repository root:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
.venv/bin/python scripts/verify_submission_results.py artifacts/results/full
```

The optional notebook execution verifier requires populated local Hugging Face caches:

```bash
.venv/bin/python scripts/verify_submission_notebook.py --notebook Phishing_Email_Triage.ipynb --mode full --save-executed
```

## Remaining human validation and measured scope

1. **Complete 30 current explanation ratings.** The active sheet is [human_explanation_ratings_9b10d09848942b57.csv](artifacts/human_explanation_ratings_9b10d09848942b57.csv), as recorded in [run_summary.json](artifacts/results/full/run_summary.json). Edit only `rater`, `correctness_1_to_5`, `grounding_1_to_5`, `usefulness_1_to_5` and `comment`. Use whole-number scores from 1 to 5 and the actual rater's name. Preserve email, verdict, reason, quote and fallback fields. Historical ratings describe their original snapshot and are not transferred.
2. **Review the revised implementation as a team.** Confirm the contributions and understand the evaluation, security policy and approval boundary. The completed presentation is preserved; the review does not establish that the team has reviewed the revised code.
3. **Keep runtime claims scoped to the tested device.** Full and quick execution succeeded on RTX 4000 Ada. No laptop/free Colab T4 run is claimed, and no additional device test is being pursued at the user's request.

After genuine ratings are entered, rerun with the same backend to validate the exact snapshot and refresh its summary. If those rated assets are published, advance the immutable artifact revision/manifest so a fresh grader workspace retrieves that same rated snapshot.

The full defended workflow still has **13 false positives and 3 false negatives** on the fixed test set. Some injection attacks still succeed. Quarantine is simulated and requires explicit analyst approval. Successful execution does not mean perfect classification or general injection immunity.

## Repository organization

One canonical notebook is published on `main`. The improvement branch's history is preserved on `main`; the merged feature branch was removed locally and from GitHub. Only the primary project checkout remains, with no additional Git worktrees. The duplicate local review notebook, model caches, virtual environment, rebuildable embeddings and intermediate checkpoints are ignored by Git.
