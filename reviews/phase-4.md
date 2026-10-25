# Phase 4 review

Reviewer: GPT-6.1-sol, reasoning effort xhigh, independent subagent.

Scope: notebook cells `p13-012`, `p13-013`, `p13-016`, `p13-027`, the Phase 4 checkpoint, and saved workflow/component checks. Earlier reviewed cell sources, model weights and fixed splits were preserved. Phase 5's full measurements, injection suite and human ratings were excluded.

Result: **Passed after direct corrections. No remaining blocking correctness findings for the bounded, simulated notebook workflow.** This does not establish production security, explanation accuracy or general robustness to prompt injection.

## Corrections made before passing

- Rejected reuse of an existing graph thread. Previously, invoking a new email on a pending thread overwrote its email and interrupt; invoking it on a completed thread retained the previous `analyst_decision`. Each `triage` call now uses an unused thread, and only `review` resumes a pending approval. Empty/non-string email inputs are rejected.
- Parsed sender claims only from the leading RFC-style header block, including folded lines. Previously, `From:` text in a quoted/body section was reported as an actual sender header. Missing headers stay missing; parsed addresses remain unverified claims.
- Marked a missing/whitespace URL host invalid. Previously, `https://` produced an empty host reported as unflagged. Existing URL deduplication and punctuation tests remain intact.
- Escaped Qwen chat-control spellings inside the explainer's JSON payload, including retrieved email text. JSON encoding alone had preserved those special tokens. The defended responder receives only the fixed classifier verdict; the declared undefended responder ablation continues to expose raw email text intentionally.
- Made explanation generation explicitly neutral and greedy, including `repetition_penalty=1.0`. The cached agent model's generation configuration uses 1.1, penalizing tokens already present in the email prompt despite the request for an exact quote. This is an explicit inference-method correction; no model, classifier prompt, threshold or weights were tuned. The existing smoke example changes from a visible quote fallback to a valid quoted model output.
- Added focused regression checks for thread isolation, non-exact decisions, sender parsing, invalid hosts, component order, training-only evidence, cache reuse, quote validation and visible fallbacks. Added a local rendered graph using the compiled graph's actual nodes/edges; Mermaid source is also retained.

## Independent verification

- Executed the full current notebook from a fresh CUDA kernel with `P13_QUICK_RUN=0`, `TRAIN=False`, cached pinned models and the reviewed saved-adapter inference path. It completed in **30.0 seconds**. All 11 current code cells have successful saved outputs; no error outputs. Notebook format and Python code syntax validate.
- Reproduced the earlier classification metrics unchanged: primary rank-8 F1 0.968610, rank-4 F1 0.958904, selected k=5 F1 0.951111, keyword F1 0.130081 and zero-shot F1 0. Both adapters were loaded, not trained; rank 8 was reloaded as the primary agent classifier. Source SHA-256 checks confirm every earlier reviewed code/narrative source in the audited set remains unchanged.
- Actual-model integration checks show no simulated quarantine before the interrupt or after rejection, exactly one log entry after approval, completed approval replay rejected, invalid decisions rejected without action, pending/completed thread reuse rejected, and safe classification allowed without an approval interrupt. Saved as `approval_checks.json`.
- Two actual-model workflow emails pass specialist order, fixed-verdict action consistency, exact nonempty quotes, training-only evidence and warmed batch-cache reuse checks. Six declared domain cases pass, including missing host; URL duplicate/trailing punctuation, body/missing/folded sender-header and fabricated-quote/fallback fixtures pass. Saved as `phase4_component_checks.json`. These are smoke checks, not estimates of component accuracy.
- In a separate process, exercised the real graph and wrappers with deterministic model stubs. Deliberately supplied the wrong raw response-model score and confirmed the defended consistency check overrides it; the undefended response remains exposed as specified. Verified separate defended/undefended cache keys, batch-cache reuse, pause/reject/approve/replay, thread isolation, unknown threads, invalid inputs, exact quote acceptance, invalid-output fallback and local parsing. The stubs isolate control flow; they do not claim model quality. Saved as `phase4_independent_checks.json`.
- With the actual pinned 1.5B tokenizer, independently confirmed single-token action labels A/B = 32/33, response prompt boundaries for both verdicts and both modes, and only the intended three role-start/two role-end tokens in an explainer prompt containing hostile control spellings in email and retrieved evidence.
- Visually inspected the locally rendered `workflow_graph.png`. The graph has a deterministic bounded supervisor schedule, returns from each specialist to the supervisor, and routes to approval only for a quarantine proposal. All indicator tools perform local parsing/string analysis; there is no mailbox or reputation/network action.

## Remaining limitations

The saved example now contains an exact quote, but the model reason incorrectly calls a phone number a link despite the extractor finding no URL. Quote validation establishes only that the quote occurs in the original email; it does not verify the reason or establish that the classifier verdict is correct. The example is preserved honestly for later failure analysis. Invalid/malformed model output uses a visibly marked template fallback rather than being counted as a successful model explanation. Real explanation quality requires the forthcoming measurements and human ratings.

Defended response selection is constrained to the LoRA verdict; the responder model alone is not the action boundary. The explanation and raw response cannot approve quarantine. Approval is a scripted notebook demonstration of the interrupt/resume mechanism, not authenticated access control for a real mailbox. Checkpoints and the simulated log are in memory and disappear on kernel restart. Each completed thread can be reviewed only once through the wrapper; the same email may still be demonstrated in a new thread.

The small brand list, edit-distance rules, URL scheme limits and absent public-suffix/reputation checking constrain the local tools. Exact quotes, escaping and these smoke checks do not prove general prompt-injection robustness. Earlier classifier truncation, bounded-input overlap and dataset/generalization limits remain as documented in Phase 3. No future test-suite results or human ratings are invented.

Phase 4 is released. Phase 5 may begin.
