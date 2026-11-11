**Implemented defence improvements — November 5, 2026**

The numerical tables below describe the saved GPU reference. They do not claim a completed run of the subsequently revised explanation guards.

The implemented workflow uses a defensively trained rank-8 LoRA adapter, two classifier views, unanimous training-only retrieval and a bounded indicator review rule. The original rank-4/rank-8 adapters remain unchanged as baselines. Analyst approval remains mandatory before every simulated quarantine. MCP still exposes only the three local indicator tools.

The new adapter continues training from the original rank-8 adapter for one epoch at learning rate 0.00005. Its 8,000 examples derive only from the original 4,000 downloaded training emails: 4,000 clean structured examples, 2,000 clean plain examples and 2,000 adversarial augmentations. True labels are retained. Requested safe/phishing labels are balanced independently of the true labels; payloads appear at different positions. Prompt and padding tokens remain masked in the label-plus-EOS objective.

The selection compares half/full checkpoints and the original two-view fallback on 400 clean validation emails and 150 development pairs. Requirements were fixed before selection: all 20 authored malicious controls quarantined, at most 12 clean false positives among 251 safe validation emails, and phishing recall at least 0.92617. Qualified candidates are ranked by malicious attacked allows, then benign attacked quarantines, then clean false positives and F1. The full checkpoint wins: 4/90 malicious attacked allows and 6/60 benign attacked quarantines on development, versus 24/90 and 11/60 for the previous defence. It has 12 clean validation false positives. Both training-only checkpoints without the indicator rule were rejected because they missed malicious controls; the refinement was confined to development data.

The two views use the same selected model: escaped JSON and escaped plain text with the untrusted-content warning. Either view may flag phishing. Retrieval uses only downloaded training emails. The existing extractor additionally requests analyst review when it observes a direct secret request with an untrusted URL, or a request to disable protection and install/run a download. Negated security reminders are tested. Exact known-brand hosts are an exception to this bounded rule, not authenticated or reputation-verified destinations. The rule has known false positives and is evaluated as an ablation.

A fresh 150-pair attack holdout was frozen before training. Its downloaded email identities are disjoint from training and development, and its payload templates are not used for augmentation or selection. Authored controls and semantically related attack families remain correlated. The checkpoint and rule were not retuned after this holdout was scored.

| Original 30 regression attacks | Defence off | Previous defence | Improved defence |
| --- | ---: | ---: | ---: |
| Malicious attacked emails allowed | 10/30 | 7/30 | 1/30 |
| Unmodified malicious controls quarantined | 10/10 | 7/10 | 10/10 |

The saved GPU off/on comparison has all 30 pairs eligible in both modes: ASR falls from 33.3% to 3.3%. The old defence's denominator excluded some already-missed controls; all outcomes remain visible in the new results.

| Fresh holdout outcome | Defence off | Previous defence | Improved defence |
| --- | ---: | ---: | ---: |
| Dataset-labelled phishing attacked emails allowed | 11/30 | 7/30 | 2/30 |
| Explicit phishing attacked emails allowed | 4/30 | 7/30 | 0/30 |
| Benign emails forced into quarantine | 26/30 | 10/30 | 2/30 |
| Authored benign emails forced into quarantine | 22/30 | 8/30 | 4/30 |
| Benign allow-directed negative controls quarantined | 2/30 | 0/30 | 1/30 |

All ten unique explicit malicious holdout controls are quarantined by the improved defence; its zero targeted successes are not caused by excluding already-missed controls. The two dataset-labelled phishing allows were already incorrect before the injected instructions. Four authored benign attacks still succeed. These outcomes do not establish general injection immunity.

There is a material clean-email tradeoff on the unchanged 300-email classification benchmark:

| Condition | False positives | False negatives | Phishing F1 |
| --- | ---: | ---: | ---: |
| Original rank-8 classifier | 3 | 4 | 0.9686 |
| Previous defended workflow | 5 | 3 | 0.9646 |
| Improved defended workflow | 13 | 3 | 0.9316 |

The security-prioritized policy was not changed after observing this test regression. New errors include legitimate seminar/recruitment messages and a technical newsletter overflagged by the review rule. The first ten displayed failures include specific evidence-based inspections. Single-view, two-view, retrieval and full-policy security ablations are reported on identical cases.

Earlier GPU full/quick executions preserve these measurements. The current source passes 34 regression tests and a real one-step CPU training/save/reload check. A partial CPU run completed baseline and validation stages; full-system generation was stopped for runtime. The revised source still needs a completed Run All and 30 human explanation ratings. Historical scores are not transferred; free Colab T4 has not been measured.

Relevant artifacts:

- `artifacts/adapters/defended-r8/training_metadata.json`: parent/input fingerprints, training parameters and frozen checkpoint selection.
- `artifacts/security/`: regenerable development and holdout specifications.
- `artifacts/results/full/defence_selection.csv`: prespecified development safeguards and candidate outcomes.
- `artifacts/results/full/security_development_metrics.csv` and `security_holdout_metrics.csv`: all-case outcomes, control accuracy, ASR denominators, same-pair comparisons and component ablations.
- `Phishing_Email_Triage.ipynb`: complete embedded implementation, saved outputs and demo; it recreates both Python helper files.

The earlier [injection audit](INJECTION_DEFENCE_REVIEW.md) is historical evidence that motivated these changes. No online learning, multimodal inspection, live mailbox or additional agent service is introduced.
