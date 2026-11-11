# Submission status

Verification date: 11 November 2026.

The implementation and saved evaluation are included on `main`. Final submission still requires the human ratings, team review and permitted-hardware check listed below.

## Submission contents

| Item | Location |
| --- | --- |
| Complete implementation, saved outputs and demo | [Phishing_Email_Triage.ipynb](Phishing_Email_Triage.ipynb) |
| Setup and running instructions | [README.md](README.md) and [requirements.txt](requirements.txt) |
| Original and defensive LoRA adapters | [artifacts/adapters](artifacts/adapters/) |
| Full classification, security and component results | [artifacts/results/full](artifacts/results/full/) |
| Frozen development and held-out attack specifications | [artifacts/security](artifacts/security/) |
| Defence changes and measured tradeoffs | [DEFENCE_IMPROVEMENTS.md](DEFENCE_IMPROVEMENTS.md) |
| Historical injection audit | [INJECTION_DEFENCE_REVIEW.md](INJECTION_DEFENCE_REVIEW.md) |
| MCP indicator server | [mcp_indicator_server.py](mcp_indicator_server.py) |
| Regression tests | [tests](tests/) |
| Presentation deck, 24 slides | [P13_Phishing_Triage_Updated.pptx](output/presentations/P13_Phishing_Triage_Updated.pptx) |
| Presentation script, demo steps and viva answers | [P13_Phishing_Triage_Full_Presentation_Script.md](output/presentations/P13_Phishing_Triage_Full_Presentation_Script.md) |

## Automated verification

- A fresh full Run All of implementation commit `9452f7e` completed on the NVIDIA RTX 4000 Ada in **194.99 seconds** excluding dependency installation (197.6 seconds for the execution harness). It used the pinned environment, cached public models and included adapters, with `TRAIN=False` and `P13_QUICK_RUN=0`. All 300 test emails were evaluated. The run was isolated from the submitted artifacts and human rating sheets.
- Fresh predictions, original injection metrics, held-out security metrics, component metrics, approval checks and MCP checks match the saved files exactly. Classification metrics match when elapsed-time columns are excluded. The current human-rating snapshot is unchanged. The saved notebook and presentation results are retained.
- All 14 regression tests pass, including live MCP stdio discovery, tool calls and invalid-argument rejection. These checks need normal subprocess access; a restricted sandbox can time out during MCP initialization.
- `pip check` reports no broken requirements. Installed versions match every pin in `requirements.txt`.
- All 21 saved notebook code cells are executed, with no saved error outputs.
- The embedded MCP and defence helper sources match the standalone Python files.
- The saved split manifest contains 4,000 training, 400 validation and 300 test emails, with disjoint email identities.
- All 37 tracked JSON files parse, and the presentation package passes its ZIP integrity check.

Reproduce the regression and dependency checks from the repository root:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

## Remaining human validation

1. **Complete 30 current explanation ratings.** The active sheet is [human_explanation_ratings_9b10d09848942b57.csv](artifacts/human_explanation_ratings_9b10d09848942b57.csv), as recorded in [run_summary.json](artifacts/results/full/run_summary.json). It currently has 0/30 valid ratings. Edit only `rater`, `correctness_1_to_5`, `grounding_1_to_5`, `usefulness_1_to_5` and `comment`; use whole-number scores from 1 to 5 and a nonblank rater name. Preserve the email, verdict, explanation and quote fields. Historical ratings remain attached to their original explanation snapshot.
2. **Have the team review the revised implementation and results.** Confirm each recorded contribution and rehearse both demo paths. An AI-assisted automated check cannot establish that the team has reviewed the work.
3. **Verify Run All on a permitted laptop or free Colab T4.** The measured RTX 4000 Ada runs do not establish runtime on those devices. Use `TRAIN=False` with the included adapters and `P13_QUICK_RUN=0` for the full 300-email evaluation. Record the actual hardware and elapsed runtime.

After entering ratings, rerun the full notebook with the same explanation backend to validate the exact snapshot and refresh the summary. Commit the completed sheet and refreshed artifacts. If the backend produces different explanations, the notebook preserves the old sheet and creates a separate snapshot; do not transfer its scores to different text.

The full defended workflow's 13 false positives, 3 false negatives and remaining injection failures are documented in the saved results. Quarantine is simulated and requires explicit analyst approval. These limitations remain part of the submission.

## Repository cleanup

The improvement branch was already merged through pull request #1. Its complete history is preserved on `main`; the merged feature branch has been removed locally and from GitHub. Only the primary project checkout remains, with no additional Git worktrees. Local model caches and the virtual environment are ignored by Git and retained for execution.
