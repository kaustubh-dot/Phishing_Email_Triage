# Submission readiness and acceptance checks

Assessment basis: [P13 project brief](P13_Phishing_Email_Triage_Team.pdf) and [Group Project Guidelines & Judging](0_Guidelines_and_Judging.pdf). The user's two-week working target is 8 November 2026.

## Current position

The six planned implementation phases are complete and independently reviewed. Commit `821de23` publishes the notebook, saved adapters, measured results and review records to GitHub. This is an implemented and locally validated project, not a completed academic submission.

The remaining mandatory closeout work is genuine human explanation ratings, actual contribution entries, required-platform reproducibility verification, and presentation/Q&A preparation. A final notebook freeze must incorporate those inputs and retain successful outputs.

## Requirements mapped to evidence

| Requirement | Current evidence | Readiness |
| --- | --- | --- |
| One notebook using the supplied structure | `Phishing_Email_Triage.ipynb`, sections 0–10 | Implemented |
| Project title, team and contribution table | Names/roll numbers present; contributions are placeholders | Team input pending |
| Problem, research question and success criteria | Notebook section 1 | Implemented |
| Versioned setup, seeds, config and QUICK_RUN | Notebook section 2; pinned dependencies and effective environment records | Implemented; published fresh clone passed |
| Named Hugging Face dataset downloaded inside notebook | `load_dataset`, immutable revision, sizes/examples/class balance | Implemented |
| Fixed stratified subsets and training-only retrieval | 4,000 train / 400 validation / 300 full test; 60 quick test | Implemented; exact bounded-input overlap disclosed |
| Keyword, zero-shot, kNN-RAG and LoRA comparisons | Shared test identities and saved predictions/metrics | Implemented |
| Required small open models and LoRA | Specified Qwen classifier/agent and MiniLM; ranks 8 and 4 saved | Implemented |
| Supervisor, indicator tools, explainer and responder | Compiled LangGraph, rendered graph and component checks | Implemented |
| Analyst interrupt before quarantine | Pause/approve/reject/replay/thread-isolation checks; simulated action only | Implemented |
| Required classification metrics, table and chart | Section 6 and `artifacts/results/full/` | Implemented |
| Rank, k and defence ablations | Rank 4/8, k=1/3/5; defence off/on | Implemented |
| Thirty injection emails and before/after measurement | 30 paired payloads over 10 malicious scenarios; paired denominators reported | Implemented; negative result retained |
| Thirty human explanation ratings | Exported rubric/sheet, all human entries blank | **0/30: mandatory human work** |
| At least ten categorized failures | Seven actual full-system failures plus three identified baseline failures, with specific AI-assisted analysis | Implemented |
| Live ask(...) demo with success and failure | Section 8; actual held-out examples and approval helper | Implemented; rehearsal pending |
| Limitations, ethics, references and AI disclosure | Sections 9–10 and notebook title | Implemented |
| Restart & Run All under 60 minutes on specified hardware | Post-correction local RTX 4000 Ada: 151.5 seconds full / 50.9 seconds quick, including kernel startup | **Laptop CPU or free Colab T4 not verified** |
| Saved outputs and accessible trained artifacts | 17 successful saved code cells; committed adapters loaded in the published fresh clone | Published snapshot and fresh-checkout checks passed |
| Ten-minute talk plus five-minute Q&A | Walkthrough is written; every member must answer a question | Rehearsal and individual understanding pending |

## Experimental findings that must remain honest

- Full classification: F1 0.9686 and accuracy 0.9767 on 300 test emails; three false positives and four false negatives.
- The validation-selected kNN baseline has F1 0.9511; zero-shot predicts all test emails safe and has phishing F1 0. The scoring implementation was independently checked.
- Only 142/300 model explanations pass format/exact-quote validation. The other 158 use visible templates. Neither exact quotes nor templates establish correctness of reasoning; no human score is available yet.
- The bundled injection defence does not improve the observed stress test: on the same 15 eligible attack pairs from five scenarios, successes are 4/15 off and 7/15 on. Raw attacked allow counts are 10/30 and 15/30. These are not independent 30-scenario trials.
- One distinct full-text training/test pair has the same truncated classifier input. A matched 299-email exclusion table is supplied; primary F1 is unchanged. This must not be described as classifier-input disjointness.

The PDFs require honest measurements and discussion. They do not specify a minimum F1 or require the defence experiment to show an improvement. Additional features are outside the agreed scope.

## Remaining work, ownership and completion conditions

1. **Human ratings — people:** a person reads each of the 30 exported emails/explanations and supplies a rater identifier plus integer correctness, grounding and usefulness ratings from 1 to 5. The notebook must then display the resulting human means. Allow approximately 1.5–2.5 person-hours, depending on reading and discussion.
2. **Contributions — team:** record actual work and review performed by each member, retaining the AI-assistance disclosure. Do not assign invented contributions. Allow approximately 30–60 minutes of discussion and edits.
3. **Required-platform run — implementation/testing:** verify a fresh-kernel full run, adapter access, memory and elapsed time on a laptop CPU or free Colab T4. The current machine is an HP Z2 desktop with a Core Ultra 9 285; a desktop CPU run would be useful compatibility evidence, but cannot be relabelled as a laptop measurement. Availability of the target platform remains a dependency.
4. **Presentation and Q&A — team:** rehearse the existing ten-minute walkthrough, success/failure demo and explicit approval decision. Every member must be able to explain their actual contribution and answer a technical question. Allow roughly 2–3 hours across preparation and timed rehearsals.
5. **Final freeze — implementation plus team:** incorporate ratings/contributions, rerun the chosen submission configuration, save outputs, confirm how the grader receives the notebook and adapters, and push the final snapshot. A repository clone already includes the adapters; a notebook-only upload needs its artifact access or training path verified. Allow 30–60 minutes after preceding work passes.

This is closeout and verification work rather than another implementation cycle. The remaining human work is approximately 4.5–7.5 person-hours, plus target-platform setup/execution and any genuine defects found by testing. A grading percentage cannot be inferred from automated review: presentation and Q&A account for 40 of the 100 marks.

## Completed detailed testing

- Verified the published GitHub branch/commit, visible README and notebook rendering in the browser.
- Executed a fresh clone with the committed adapters and notebook, independent of unpublished authoring scripts and local project state.
- Recomputed split/metric/ablation/pairing evidence and verified the human-rating blanks and failure counts against the PDFs.
- Exercised input, tool, explanation, approval and thread boundaries using targeted cases; probed CPU/backend compatibility without claiming unmeasured laptop/T4 timing.
- Fixed the confirmed rating-snapshot defect within notebook scope, completed affected checks, and passed GPT-6.1-sol xhigh independent review before follow-up publication.

Detailed results are in [DETAILED_TESTING.md](DETAILED_TESTING.md). The published fresh clone passed in 291.6 seconds with an empty model/data cache; post-correction quick/full GPU runs passed in 50.9/151.5 seconds. A two-case real CPU probe found and verified the rating-snapshot correction. None of these results is relabelled as a full laptop CPU or Colab T4 run. The bounded testing checkpoint passed GPT-6.1-sol xhigh independent review; see [reviews/submission-testing.md](reviews/submission-testing.md). Human closeout and required-platform verification remain pending.
