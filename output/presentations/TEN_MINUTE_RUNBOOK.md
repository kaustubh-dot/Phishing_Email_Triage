# Ten-minute presentation and five-minute Q&A

Finish Run All before the talk. Keep the notebook kernel and its cached outputs open. The main deck is slides 1–18; slides 19–24 are for Q&A. Numerical deck tables are the labelled saved GPU benchmark. The notebook and CPU verification record report the actual final CPU execution separately.

| Clock | Slides | Show and explain |
| --- | --- | --- |
| 0:00–0:10 | 1 | Team and project question |
| 0:10–0:50 | 2–3 | Analyst queue, classification and injection questions |
| 0:50–1:20 | 4 | Downloaded dataset, seed 42, disjoint splits and subset sizes |
| 1:20–2:20 | 5–6 | Four roles, training-only evidence and unchanged baselines |
| 2:20–3:40 | 7–9 | Original vulnerability and label-preserving defensive training |
| 3:40–4:10 | 10 | Real MCP tool discovery and one actual tool call |
| 4:10–4:40 | 11 | Two views, retrieval/rule corroboration and separate approval |
| 4:40–5:40 | 12 | Current success example and explicit analyst approval |
| 5:40–6:40 | 13 | Actual error, evidence inspection and rejection when pending |
| 6:40–7:25 | 14 | Same-subset metrics and clean-email false-positive cost |
| 7:25–8:10 | 15 | Before/after injection outcomes and conditional denominators |
| 8:10–8:40 | 16 | Quote/format limits and snapshot-specific human ratings |
| 8:40–9:20 | 17 | At least ten distinct failures and validation follow-ups |
| 9:20–9:50 | 18 | Tested hardware, limits and completed human review |
| 9:50–10:00 | — | Transition to Q&A |
| Next five minutes | 19–24 | Use only the appendix needed for each answer |

## Live success

Create a fresh thread so an earlier approval cannot be replayed:

```python
demo_success_thread = ask(test_df.iloc[demo_success_index].text)
```

Read its actual verdict, neighbour labels/similarities, tool results, reason, exact source quote and fallback flag. A nonfallback flag does not establish useful reasoning. Then act as the analyst:

```python
review(demo_success_thread, 'approve')
```

Confirm the simulated action occurs only after approval. Do not rerun that approval on a completed thread.

## Live failure

Use the first observed full-system error, not an invented failure:

```python
failure_index = int(np.flatnonzero(PREDICTIONS['Full system (defended)'] != truth)[0])
demo_failure_thread = ask(test_df.iloc[failure_index].text)
```

Compare the actual dataset label with the workflow verdict. If the false-positive quarantine is paused, reject it:

```python
review(demo_failure_thread, 'reject')
```

If the error is an allowed phishing-labelled message, explain the missed alert instead; that path has no quarantine approval to reject. Keep dataset ambiguity, limited evidence and false-positive costs distinct.

## Claims to keep precise

- The project owner confirmed personally completing all 30 human reviews of the submitted explanation cases. The completion record states that source; historical numeric means retain their original snapshot scope.
- Source-matching quotes and valid JSON do not prove semantic correctness. The copy and word-budget guards reject specific weak outputs and retain visible fallbacks.
- The original injection suite contains 30 variants over 10 base scenarios. It does not represent 30 independent campaigns.
- Security improvements have a clean-email false-positive cost. No threshold or policy is selected on the scored holdout.
- State the actual device and cache assumptions for each timing. GPU reference timings are not CPU timings.
- Each person should explain the code and decisions in their recorded contribution, including the masked LoRA loss, training-only index, supervisor, exact quote handling and approval boundary.
