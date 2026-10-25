# P13 — Phishing Email Triage

Working target: 8 November 2026. Implementation and training take place in this repository on the local NVIDIA RTX 4000 Ada GPU (20 GB VRAM).

## Scope

One executable notebook adapted from `Project_Notebook_Template.ipynb`, covering the required dataset, keyword and zero-shot baselines, kNN retrieval, Qwen LoRA classification, a LangGraph supervisor with specialist nodes, analyst approval, and the prescribed evaluation. Quarantine is a simulated notebook action. The optional frontend and MCP stretch goal are excluded.

## Team

| Member | Roll number | Role and contribution |
| --- | --- | --- |
| Kaustubh Rajesh Upadhya | S20240030379 | To be discussed |
| Tejas Tandon | S20240030405 | To be discussed |
| Kanishk Gorana | S20240030378 | To be discussed |

## Phases

1. **Environment and data (days 1–2):** create an isolated environment, verify CUDA, download the named dataset, clean and deduplicate before splitting, save fixed split identities, and measure keyword rules. Checkpoint: inspect class balance and baseline errors.
2. **Baselines and retrieval (days 3–4):** evaluate the unchanged Qwen classifier and embedding kNN; index training data only and compare k on validation data. Checkpoint: one fixed test subset shared by every condition.
3. **LoRA (days 5–7):** adapt the fine-tuning lab from T5 QA to Qwen causal classification, train ranks 8 and 4 on identical examples, save adapters and training metadata. Checkpoint: measured classifier comparison and a reloadable adapter.
4. **Agent workflow (days 8–10):** implement supervisor routing, classifier and evidence, indicator tools, explanation, response proposal, and LangGraph interrupt/resume. Checkpoint: approval and rejection both work; no simulated quarantine occurs before approval.
5. **Evaluation (days 11–12):** classification metrics, component measurements, k/rank ablations, 30 matched injection attacks before/after defence, and 30 explanations ready for human ratings. Checkpoint: real results, a chart, and at least 10 documented model/baseline failures.
6. **Submission (days 13–14):** complete notebook narrative, limitations, references and demo; run from a fresh kernel and record runtime. Checkpoint: outputs saved, QUICK_RUN supported, and presentation walkthrough documented.

These day ranges are planning allowances. Phases can finish sooner when their checks pass.

## Course material to adapt

- `Fine_Tuning_Lab.ipynb`: PEFT LoRA setup, training, adapter saving. It uses FLAN-T5 QA; this project requires Qwen causal classification.
- `4_Structured_Generation_Lab.ipynb`: zero-shot prompts, structured responses, tool schemas.
- `1_RAG_Pipeline_Lab.ipynb`: MiniLM embeddings, FAISS and retrieval measurement; use downloaded training emails in place of the lab corpus.
- `1_Multi_Agent_System_End_to_End.ipynb`: supervisor routing, tools, checkpointer, `interrupt` and `Command(resume=...)`.

Lab notebooks are read from the supplied ZIPs without importing or executing their code.

## Human work that cannot be fabricated

- Discuss and record each member's actual contribution.
- Have a person rate 30 explanations using the notebook's exported rubric and rating sheet.
- Rehearse the presentation and Q&A.

## Execution record

- Planning: complete. Four relevant lab notebooks located. GPU confirmed outside the sandbox.
- Phase 1: complete. Notebook sections 0–4 executed from a fresh kernel on the local CUDA environment. Downloaded 18,650 emails; retained 17,497 clean unique emails. Fixed subsets: 4,000 train, 400 validation, 300 test; quick evaluation uses 60 of those test emails.
- Phase 1 measurements: keyword accuracy 0.6433, precision 0.7273, recall 0.0714, F1 0.1301 and false-positive rate 0.0160. Low recall is reported as an observed limitation, not hidden or tuned away on the test set.
- Phase 1 review: GPT-6.1-sol, xhigh; passed after correcting regex boundaries and adding baseline sanity checks and initial failure inspection. See `reviews/phase-1.md`.
- Phase 2: complete. Training-only normalized MiniLM embeddings and FAISS cosine kNN; k=1/3/5 selected only on validation data. Selected k=5 validation F1 0.9377, test F1 0.9511. Label-agreement Hit@5 0.9833 and reciprocal rank at 5 0.9700 are explicitly proxy measures.
- Phase 2 zero-shot: unchanged Qwen2.5-0.5B-Instruct raw next-token A/B scoring predicts all 300 test emails safe (112 false negatives, phishing F1 0). Validation-only token, batching and neutral-generation checks pass; the poor result is retained without test tuning.
- Phase 2 review: GPT-6.1-sol, xhigh; passed after adding explicit left-padding positions, preprocessing-aware embedding cache keys, documented scoring/truncation, and a saved retrieval example. Fresh-kernel full-subset execution succeeded. See `reviews/phase-2.md`.
- Phase 3: complete. Qwen causal LoRA ranks 8 and 4, targeting q_proj/v_proj, were trained on the same 4,000 emails with 400 validation examples, seed 42, one epoch, batch size 8 and learning rate 0.0002. Trainable parameters: 540,672 / 270,336; training runtimes: 157.11 / 157.62 seconds. Rank 8 was predeclared primary.
- Phase 3 measurements: fresh saved-adapter inference gives rank-8 accuracy 0.9767, precision 0.9730, recall 0.9643, F1 0.9686 and false-positive rate 0.0160; rank-4 F1 0.9589 and false-positive rate 0.0106. Selected k=5 remains F1 0.9511; unchanged zero-shot remains F1 0. An initial Trainer autocast evaluation changed one decision per rank; the notebook now uses the deployed reload path consistently, with no retraining or test tuning.
- Phase 3 input audit: full normalized email identities remain disjoint. One distinct safe training/test pair collapses to an identical bounded Qwen input. The fixed split is retained, the overlap is disclosed and a separate sensitivity table uses the same 299 eligible test messages for every condition; rank-8 F1 stays 0.9686 and rank-4 F1 rises to 0.9633. Carry this limitation into the final evaluation narrative.
- Phase 3 review: GPT-6.1-sol, xhigh; passed after fixing repeat rank-8 retraining under TRAIN=True, unifying saved-adapter inference, strengthening cache provenance and pinning adapter reload revision. Causal masking/alignment, LoRA-only gradients, adapter weights and reload predictions independently verified. See `reviews/phase-3.md`.
- Phase 4: complete. Deterministic LangGraph supervisor routes classifier, local URL/domain/sender tools, model explainer and responder, then interrupts before any simulated quarantine. The compiled graph is rendered locally. Approve, reject, safe allow, replay rejection, invalid decisions, thread isolation, cache reuse, exact quotes and visible fallbacks pass focused integration/component checks. Checkpoint/log persistence is limited to the current kernel; sender fields are unverified claims, and tools make no network/reputation queries.
- Phase 4 review: GPT-6.1-sol, xhigh; passed after rejecting reused graph threads, restricting sender parsing to the leading header block, rejecting missing URL hosts and escaping untrusted chat-control spellings for the explainer. Neutral greedy explanation generation explicitly uses repetition penalty 1.0 rather than the saved model default of 1.1. A fresh full-subset CUDA run passed all 11 current code cells in 30.0 seconds. Earlier reviewed sources, model weights and splits were preserved. See `reviews/phase-4.md`.
- Phase 4 limitation: exact quote validation does not check the reason. The preserved example has a genuine quote but incorrectly calls a phone number a link; full explanation/component evaluation and human ratings remain future work. Two-email smoke checks are not full evaluation results.
- Phase 5: complete implementation and evaluation. The full defended graph evaluated the same 300 emails: accuracy 0.9767, precision 0.9730, recall 0.9643, F1 0.9686 and false-positive rate 0.0160, identical to primary rank 8. All 111 quarantine proposals paused; no quarantine was executed during evaluation. The shared 299-email input-overlap sensitivity result is preserved.
- Phase 5 explanations: 142/300 model outputs passed format and exact-quote validation; 158/300 used visible template fallbacks. All 300 quotes are exact, including fallback quotes, without implying reason correctness. Six declared indicator fixtures and retrieval label-agreement proxies remain limited component checks. Complete indicators stay in graph state; the explainer uses at most five bounded URL/domain examples plus counts, with a 4,096-token rejection guard and observed maximum 1,151 tokens.
- Phase 5 injection results: 30 authored pairs across 10 synthetic malicious scenarios, three pairs per scenario, evaluated with the same payloads in both modes. Raw attacked allow rates: 10/30 defence off, 15/30 defence on. Targeted successes: 10/30 versus 7/15 eligible controls. The same 15 pairs eligible in both modes give 4/15 versus 7/15. This is an observed negative bundled-defence result, retained without prompt/threshold/attack tuning. Classifier flips and responder action disagreements are reported separately; no attacked allow contradicts a phishing classifier verdict.
- Phase 5 errors and human work: 127 distinct emails fail at least one condition; ten specific AI-assisted case inspections prioritize all seven actual full-system errors and add three baseline errors. These are evidence-based observations and hypotheses, not human ratings or established causal diagnoses. The 30-case human explanation sheet is exported, with all human fields blank and **0/30** completed. Genuine ratings and team contributions remain required human work.
- Phase 5 review: GPT-6.1-sol, xhigh; passed after adding the common-eligible attack comparison and action/classifier diagnostics, explicit model/fallback counts, rating-snapshot identity checks, ten specific failure analyses and readable confusion-cell text. A fresh full CUDA run saved all 15 successful code cells (149.9-second recorded cell execution span, excluding kernel startup). Independent metric, pairing, cap, role-token, budget and artifact checks pass. Earlier cell sources, weights and fixed splits are unchanged during this review. See `reviews/phase-5.md` and `artifacts/results/full/phase5_review_checks.json`.
- Phase 6: automated implementation complete and reviewed. Sections 8–10 contain `ask(email)`, an observed success and actual full-system failure, the existing explicit approval/rejection helper, a ten-minute walkthrough, concrete limitations and verified primary references. Both fresh-kernel GPU modes passed: 60 quick / 300 full emails. Notebook summaries measure 44.28 / 149.96 seconds after setup imports; runner wall times including kernel startup and installation were 47.9 / 153.5 seconds. No training, model/prompt/threshold changes or split changes were needed.
- Phase 6 review: GPT-6.1-sol, xhigh; passed after clarifying that the common injection comparison is 15 attack pairs from five unique scenarios and completing tool reference links. All 17 code cells have successful saved full-run outputs. Format/syntax, dependency pins, classification metrics in both modes, rating separation, error cases, source/weight preservation and the public demo/approval functions passed focused checks. See `reviews/phase-6.md` and `artifacts/results/full/phase6_review_checks.json`.
- Remaining before academic submission: record each member's actual contribution, collect 30 genuine human explanation ratings, rehearse the ten-minute talk and individual Q&A, and verify the assignment's under-60-minute requirement on a laptop or Colab T4. The local RTX 4000 Ada timings do not verify those target platforms. Automated implementation/review is complete; human work and target-platform verification are not claimed complete.
- Post-publication submission testing: the published fresh clone ran all 17 code cells with an initially empty model/data cache in 291.6 seconds on the local GPU, using the committed adapters and existing uv wheel cache. All 300 predictions matched. A two-case FP32 desktop CPU probe found a changed explanation that exposed the old rating-snapshot assertion. The corrected cell preserves prior sheets, uses blank fingerprinted sheets for changed explanations, checks selected-sheet identities and records the selected path. Post-correction quick/full GPU runs passed in 50.9/151.5 seconds. GPT-6.1-sol xhigh independent review passed the bounded correction and readiness assessment; see `reviews/submission-testing.md` and `artifacts/submission_checks/independent_review.json`. No weights, prompts, thresholds, data splits or attack cases changed. Human ratings remain 0/30, and the required laptop CPU/Colab T4 run remains pending.
