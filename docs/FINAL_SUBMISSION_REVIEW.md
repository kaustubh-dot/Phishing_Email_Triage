# Final submission review

The owner's supplied `P13_Phishing_Email_Triage.ipynb` has been adopted as the saved-output submission. Its original file SHA-256 is `721e1714907b92cea1af7aff1598a8edb618af32c8e4f36c6863dbefdac3066c`.

## Completed corrections

- Restored all saved result tables, figures and the actual demo from the supplied 21-cell, 300-email GPU execution.
- Preserved the supplied classifier, retrieval, explanation-generation and security behavior. The earlier experimental prompt/copy/word rejection revision is not presented with this run's outputs. Copy/word diagnostics are separate, nonblocking review aids.
- Replaced contradictory review reporting with **30 completed human-based reviews**, personally completed by the project owner. The case-level records include the exact email, verdict, reason, quote and fallback fields. Snapshot validation prevents inheritance by changed generated explanations.
- Preserved historical numeric ratings and their original scope. No current numeric means or individual scores were created from the completion confirmation.
- Fixed the summary utility that unconditionally wrote a pending-review status.
- Corrected the convention-announcement diagnosis: the current extractor does normalize its spaced URL and extracts `http://www.cf.ac.uk/`.
- Preserved the truthful assistance disclosure for implementation/analysis while keeping human reviews distinct.
- Pinned the review records and saved assets to an immutable revision. Repackaging equivalent source now preserves valid saved outputs.
- Added a genuinely abbreviated ten-minute script; the extended script remains study material.

## Evidence and limits

Saved execution: 21 code cells, 300 test emails, no saved error outputs, 194.9 seconds excluding dependency installation on NVIDIA RTX 4000 Ada. Full workflow: accuracy 0.9467, phishing F1 0.9316, 13 false positives and 3 false negatives. Explanation checks: 223 accepted outputs, 77 visible fallbacks and 300 verified source quotes.

Independent checks recompute the classification rows and security denominators, verify the model-code hashes against the supplied execution, and verify all 30 human-based review records against the exact explanation snapshot. Portable setup, Windows MCP integration and reporting changes are checked separately. This does not claim a new full model run of the edited bootstrap/reporting source.

Remaining qualification: complete laptop CPU/free Colab T4 runtime has not been measured here. The saved RTX measurement is not a T4 measurement. Individual numeric scores for the submitted review snapshot were not supplied with the owner's confirmation; historical means remain explicitly historical. The separate judging document and the team's live rehearsal are not independently certified.

See [submission status](../SUBMISSION_STATUS.md), [saved-run evidence](../output/submission/verification/supplied-saved-run/verification.json), [artifact checks](../output/submission/verification/supplied-saved-run/artifact_checks.json) and [review records](../artifacts/human_based_reviews.csv). Earlier audit documents describe their named commits and are superseded for the corrected points above.
