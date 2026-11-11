# Historical injection-development audit

These files are the diagnostic audit of the original adapters and earlier inference defences. They motivated the subsequent adversarial LoRA training, two classifier views and bounded review policy. The report is [INJECTION_DEFENCE_REVIEW.md](../../../INJECTION_DEFENCE_REVIEW.md).

The audit includes clean validation, frozen development challenge cases, paired control/attack outcomes, prompt-format ablations and runtime provenance. Its development cases were inspected during implementation; they are not an unseen final security benchmark.

For current outcomes, use [the full-run security metrics](../full/security_holdout_metrics.csv), [current selection records](../full/defence_selection.csv) and [DEFENCE_IMPROVEMENTS.md](../../../DEFENCE_IMPROVEMENTS.md). The reproduction script [audit_injection_defences.py](../../../scripts/audit_injection_defences.py) intentionally uses the original adapters and reference actions, rather than evaluating the current policy.
