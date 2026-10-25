# Detailed submission testing

Acceptance sources: [project brief](P13_Phishing_Email_Triage_Team.pdf) and [guidelines/judging](0_Guidelines_and_Judging.pdf). Testing is limited to the required notebook, models, evaluation, demo, reproducibility and submission artifacts.

## Published snapshot and browser check

Commit `821de23072bd435acc7983a2d183729fa6ffc9a4` was pushed to `main` and verified using GitHub's branch reference and the browser. The public README renders, and GitHub's notebook preview displays the title/team, all sections 1–10, saved code outputs, evaluation, actual success/failure demo and explicit 0/30 human-rating status. This is a rendering check; GitHub's preview is not a notebook execution service. No application frontend is required or added.

## Fresh-checkout execution

- Cloned the published repository into a new temporary directory.
- Created a separate Python 3.12 environment and installed all committed pins. Dependency wheels reused the existing uv package cache; this was not a cold package-download timing.
- Started with an empty Hugging Face model/data cache in the clone, downloading the specified public dataset/models and rebuilding training-only embeddings.
- Executed all 17 code cells from a fresh kernel, loading the committed adapters rather than retraining.
- Completed in **291.6 seconds** on the local RTX 4000 Ada GPU, including kernel startup, notebook setup and model/data downloads.
- All 300 prediction rows matched the published full-run results. No unpublished authoring script is called by the notebook.

Evidence: `artifacts/submission_checks/fresh_checkout.json` and `browser_check.json`.

## CPU compatibility finding and correction

A targeted real-model CPU probe used FP32 inference for two existing cases. One generated reason differed from its GPU counterpart. The original rating-sheet identity assertion then blocked the run because the published sheet described different text. Classification and the quarantine gate behaved correctly; this was a rating-snapshot portability defect.

The corrected cell preserves existing sheets and human entries. A different email/explanation snapshot gets a separate fingerprinted sheet with blank human fields. Only ratings for matching immutable text are counted. Reordering rows is accepted by case identity. A nonmatching canonical legacy sheet is preserved and isolated; the code cannot identify whether its mismatch came from a prior backend or an edit. If the selected fingerprinted sheet already exists, altered immutable text, schema or case identities are rejected. No mismatching sheet supplies scores to the current explanations. The run summary records the actual sheet path.

The corrected real CPU probe completed in **33.55 seconds** and passed the affected rating path. Tests also covered initial sheet creation, existing scores, reordered rows, changed reasons, no transfer of scores to new explanations, and rejection of immutable-field tampering. Temporary synthetic rating fixtures were used only to test preservation; they are not human ratings and were never entered in the project's rating sheet. All genuine project human fields remain blank.

Evidence: `cpu_probe_before_fix.json` and `cpu_probe_after_fix.json`. This is a two-case compatibility probe on a desktop CPU, not a complete CPU benchmark or laptop timing.

## Post-correction execution and acceptance checks

Quick mode passed from a fresh GPU kernel in **50.9 seconds**, and the final full run passed in **151.5 seconds**, including kernel startup and the installation cell. Their notebook-only after-setup times are 47.19 and 147.93 seconds. All 17 full-run code cells have successful saved outputs. The acceptance checks and GPT-6.1-sol xhigh independent review passed; see [reviews/submission-testing.md](reviews/submission-testing.md).

The focused acceptance checks recompute classification metrics and common attack denominators; verify shared test identities, the overlap sensitivity and ten inspected failures; check that human fields remain blank; and exercise the actual notebook's public demo, graph and approval functions with explicitly labelled saved-output fixtures. Fixture control tests do not claim new model inference or genuine analyst decisions. Real model execution is covered separately by the complete GPU runs and targeted CPU probe.

No model weight, training objective, classifier prompt/threshold, split or injection payload was changed to obtain better results. The only executable correction addresses rating snapshots and records the selected sheet path.

Independent review executed the actual rating cell against temporary synthetic fixtures, covering first creation, prior scores, reordered rows, changed explanations, no score transfer, selected-sheet tampering/schema/identity checks and quick/full separation. It independently recomputed both modes' classification metrics and verified preserved published weights, split/revision/attack files and genuine blank rating sheets. Evidence is in `artifacts/submission_checks/independent_review.json`. It used the already completed real-model run outputs rather than repeating model execution.

## Requirements still pending

- **30 genuine human explanation ratings**, followed by saved human metrics.
- **Actual contribution entries** for the three members.
- **Ten-minute presentation and five-minute Q&A rehearsal**, with every member able to answer a question about their work.
- **The specified target-platform timing**: free Colab T4 or laptop CPU. The available machine is an HP Z2 desktop; the local GPU and targeted desktop CPU results do not certify that exact requirement.
- **Final submission freeze** after those inputs, including confirmation that the grader can obtain the notebook and saved adapters through the accepted submission mechanism.

The negative injection result, explanation fallback rate and bounded-input overlap remain disclosed. Passing implementation tests is not a claim that these research limitations have disappeared or that the academic submission is complete.
