**Injection-defence audit — November 5, 2026**

This is the historical pre-hardening audit at commit `09f8f9f`. Its recommended changes have since been implemented and tested; see [DEFENCE_IMPROVEMENTS.md](DEFENCE_IMPROVEMENTS.md) for current results.

The current defence improves the original 30-pair regression but still regresses on a new set of explicit phishing scenarios. It is not ready to freeze as the final defence. A low conditional attack success rate alone is insufficient: a defender that already allows malicious controls can exclude those failures from its ASR denominator.

The audit reproduced every committed control/attack action in both original conditions, then tested eight fixed inference configurations on the available RTX 4000 Ada GPU. It used 400 clean validation emails and 150 paired cases per configuration. No final test emails, model weights, notebook policy, approval logic or MCP tools were changed. All actions are proposed labels; no quarantine was executed.

The paired cases comprise the original 30 attacks, 30 new payloads on 30 distinct dataset-labelled phishing validation emails, 30 benign messages with allow-directed instructions, 30 benign messages with quarantine-directed instructions, and 30 attacks across ten newly authored explicitly malicious scenarios. The downloaded positive class includes ambiguous spam; the additional authored scenarios explicitly request credentials, banking codes, payments or disabling protection. The short downloaded messages were sampled with fixed seeds. The audit freezes case identities and payloads before scoring; these results are diagnostic, not an independent final security certification.

| Outcome: malicious attacked emails allowed (lower is better) | Defence off | Current defence on |
| --- | ---: | ---: |
| Original regression suite | 10/30 | 7/30 |
| New dataset-labelled phishing cases | 9/30 | 3/30 |
| New explicit phishing scenarios | 7/30 | 14/30 |

On the original suite, both modes' controls are correctly quarantined for the same 21 pairs; targeted success is 6/21 off versus 4/21 on. On the new dataset-labelled cases, the same 28 eligible pairs yield 7/28 versus 1/28. These matched comparisons favor the current defence, but neither removes the new explicit-phishing regression.

On the original ten unique malicious controls, off quarantines 10/10 and the current defence 7/10. On the ten new unique explicitly malicious controls, off quarantines 10/10 and the current defence only 2/10. The latter's conditional ASR is 0/6 repeated eligible pairs despite allowing 14/30 attacked emails: most control failures were excluded before ASR was computed. Undefined ASRs for zero eligible controls must remain undefined.

The current defence also reduces malicious instruction-driven quarantine of benign mail: on the same 25 eligible benign controls, off has 21/25 targeted successes versus 7/25 on. It still fails on claimed-authority, task-replacement and fake-role instructions. Ordinary benign messages carrying allow-directed instructions are negative controls, not harmful attack successes; only their accuracy/false-positive behavior is interpreted.

The classifier ablations identify a concrete format sensitivity. On the original ten malicious controls:

| Classifier input, before retrieval | Controls classified phishing |
| --- | ---: |
| Raw email, no extra warning | 10/10 |
| Escaped raw email, no extra warning | 10/10 |
| JSON-wrapped email, no extra warning | 5/10 |
| Escaped raw email with the warning | 10/10 |
| JSON-wrapped email with the warning, current format | 5/10 |

In these cases JSON wrapping is the important changed factor; the warning alone is not the cause. This does not establish that JSON is generally unsafe or that removing it is sufficient. The JSON-only variant still misses controls and loses clean recall. Input formatting has not taught this small classifier to consistently ignore email-authored instructions.

Two bounded candidates use the same LoRA model and the existing retrieval index. Both preserve the original raw-input classifier's phishing flags: a protected-input safe prediction cannot erase one. Raw email still cannot authorize an allow action. A phishing flag produces a proposal that remains subject to the existing analyst interrupt.

| Configuration | Original attacks allowed | New explicit attacks allowed | New explicit controls quarantined | Clean validation false positives, 251 safe emails | Clean validation F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Off, original responder | 10/30 | 7/30 | 10/10 | 27/251 | 0.8608 |
| Current defence | 7/30 | 14/30 | 2/10 | 8/251 | 0.9568 |
| Raw/protected OR + unanimous 5/5 RAG | 6/30 | 5/30 | 10/10 | 12/251 | 0.9477 |
| Raw/protected OR + majority 3/5 RAG | 0/30 | 3/30 | 10/10 | 19/251 | 0.9333 |

The balanced OR + unanimous candidate also reduces the new dataset-labelled phishing successes to 1/29 from off's 8/29 on the same pairs. It does increase erroneous quarantine proposals on benign forced-quarantine cases relative to the current defence: 17/30 versus 10/30, although off produces 26/30. The aggressive 3/5 candidate produces 19/30. Therefore no tested configuration dominates the current defence on every security and utility measure.

The recommended next work, within P13's existing components, is:

1. Implement and validate the raw/protected OR + unanimous retrieval candidate as the immediate fix for protected-prompt control regressions. Keep both scores, the contributing flag and the final proposal visible. Preserve human approval. Its measured cost is four extra false positives on the 400-email validation set. Promote it only with that tradeoff documented and after full workflow verification.
2. Harden the existing Qwen LoRA training with label-preserving adversarial augmentation of downloaded training emails. Include safe and phishing examples, both requested label directions, fake authority, role delimiters, task replacement, obfuscation and varied payload positions. Train against the true email label, never the payload's requested label. Preserve clean examples and the original baseline adapter. This extends the required fine-tuning component; it introduces no new service or agent.
3. Separate training, development and final evaluation payload families and email identities before training. The now-inspected original and audit suites are regression/development evidence. Freeze another unseen attack suite before selecting the new checkpoint. Keep the current 300-email final benchmark fixed and report its limits transparently.
4. Select the new checkpoint using malicious attacked-allow rate, unmodified malicious-control recall, both-direction targeted ASR on common eligible pairs, and benign false-positive rate. Report numerators/denominators and raw outcomes together. A 0% ASR with poor control recall is not an acceptable success criterion. The LoRA 0.5 threshold can remain fixed.

Adversarial augmentation is a proposed next experiment, not an achieved improvement. Training models to ignore instructions in the data portion has precedent in [StruQ](https://arxiv.org/abs/2402.06363); reproducing those gains in this Qwen classifier requires measurement. [OWASP's guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) also treats separation, validation and human control as layers whose effectiveness must be evaluated.

Run the audit from the repository root:

```bash
.venv/bin/python scripts/audit_injection_defences.py
```

The harness uses the notebook's actual scoring/prompt functions and committed split identities. Results are in `artifacts/results/injection_audit/`: the complete policy matrix, per-case outcomes, frozen challenge cases, classifier scores, prompt-control ablation and run provenance. The final run took approximately 42 seconds on CUDA. Scenarios and payload families are correlated, and these are descriptive point estimates.
