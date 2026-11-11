# Ten-minute presentation script

Use slides 1-18. Aim to finish by 9:40 and reserve five minutes for Q&A. This is the delivery script; the extended presentation script is study material. Bracketed actions are not spoken. Timing includes two short live demonstrations. Rehearse with the actual machine and shorten pauses where needed.

## 0:00-0:40 - Slides 1-3

We built a phishing-email triage team for an analyst who cannot manually inspect every reported message. The system classifies the email, retrieves similar labelled examples, extracts indicators, explains the verdict and proposes an action. Every quarantine proposal pauses for a person's approval.

We ask two questions. Does LoRA improve a small classifier over keyword rules, zero-shot prompting and embedding kNN? Can a defence reduce attacks that tell the model to ignore the email and return a safe label? Classification quality and resistance to instructions inside the email are measured separately.

## 0:40-1:25 - Slide 4

The notebook downloads the specified public Hugging Face dataset at a pinned revision. After cleaning and deduplication, it uses 4,000 training emails, 400 validation emails and a fixed 300-email test subset, selected with seed 42. The test subset contains 188 safe and 112 phishing-labelled emails.

Full email identities are disjoint across splits. One bounded classifier input still overlaps after truncation, and near-copy campaigns remain. We disclose that limitation and retain a common 299-email sensitivity table. These are fixed-split measurements, not proof of general enterprise-email performance.

## 1:25-2:20 - Slides 5-6

The classifier is Qwen2.5-0.5B-Instruct with LoRA. Rank 8 is the primary model and rank 4 is an ablation. Training loss covers the A/B label and EOS, while prompt and padding tokens are masked. Saved adapters and their training fingerprints are included.

MiniLM embeddings and FAISS provide the kNN baseline and labelled evidence for explanations. The index contains training emails only. We compare k values 1, 3 and 5 and choose k on validation data.

A deterministic LangGraph supervisor routes the classifier, extractor, explainer and responder. The explainer/responder use the permitted small Qwen agent model. Local tools inspect URL spellings and sender-header claims; they do not authenticate senders or visit websites. Quarantine is simulated, and the email or model cannot approve it.

## 2:20-3:30 - Slides 7-9

Early defence results exposed a problem: hiding an instruction in email text could change the classification or make the responder allow a still-suspicious email. Conditional attack rates could also conceal controls that were already missed.

The improved defence continues rank-8 training using 8,000 examples derived only from the 4,000 training identities. It combines clean structured examples, clean plain examples and label-preserving adversarial examples. Requested labels vary independently of the real labels.

Checkpoint selection uses development data subject to clean-error and malicious-control safeguards. The fresh holdout is frozen before selection and excluded from training. We preserve all raw outcomes and compare common eligible pairs. The original rank-4 and rank-8 adapters remain unchanged baselines.

## 3:30-4:10 - Slides 10-11

The MCP server exposes the same three local indicator functions over stdio. Discovery, real calls, parity and invalid arguments are checked. No quarantine action is exposed through MCP.

The defended classifier checks escaped structured and plain views. Either view can flag phishing. Unanimous training-neighbour evidence and a bounded indicator rule can also request review. The responder is constrained to the resulting verdict. These layers improve security on the tested cases but can increase false positives.

## 4:10-5:15 - Slide 12: live success

[Create a fresh thread: `demo_success_thread = ask(test_df.iloc[demo_success_index].text)`.]

This is an actual held-out prediction. Compare the dataset label and verdict, then inspect the quote, retrieved labels and indicators. Check the fallback flag: a verified quote does not by itself prove a useful explanation. This selected example illustrates the measured workflow; it does not change test membership or tune the classifier.

The quarantine proposal is waiting. I now act as the analyst.

[Run `review(demo_success_thread, 'approve')` if the proposal is pending.]

Only that explicit approval records the simulated action. Replaying approval on a completed thread is rejected.

## 5:15-6:20 - Slide 13: live failure

[Create a fresh thread for the first observed full-system error.]

This is an actual error, not an invented failure. Compare the true label with the workflow verdict. Look at the visible email evidence, quote and neighbour labels before proposing a cause. Promotional or technical language can be overflagged even when there is no visible credential request.

[Reject a pending false-positive proposal with `review(demo_failure_thread, 'reject')`. For an allowed phishing-labelled error, explain the missed alert instead.]

Rejecting a proposal prevents action. It does not retrain the classifier or update the retrieval index. Further changes would need development-only assessment and a new frozen evaluation.

## 6:20-7:15 - Slide 14

All ten conditions use the same 300 emails. Original rank-8 LoRA reaches phishing F1 0.9686, with three false positives and four false negatives. The full defended workflow reaches F1 0.9316, with thirteen false positives and three false negatives.

The stronger policy therefore reduces some misses and increases unnecessary review. We report that clean-email cost openly. Zero-shot predicts all safe under the declared constrained A/B method; its F1 is zero on this split. The score compares two label logits and is not a calibrated real-world probability.

## 7:15-8:00 - Slide 15

The original injection suite contains thirty variants over ten malicious base scenarios. All thirty paired controls are eligible in both modes. Targeted success falls from ten of thirty with defence off to one of thirty with defence on.

The separate holdout includes malicious and benign targets and negative controls. The appendix retains control correctness, all attacked outcomes and conditional denominators. Related scenarios are correlated, and some attacks still succeed. These results do not establish general injection immunity.

## 8:00-8:45 - Slide 16

The saved run has 223 model outputs passing schema, exact-span and limited factual checks, and 77 visible template fallbacks. All displayed quotes match their email source. Those checks do not prove that the reasoning is correct or useful.

Thirty human-based reviews were personally completed by the project owner. The records are bound to the exact saved case text. Historical numeric means remain attached to their original explanations; they are not transferred to changed text. Assistance with implementation and analysis is disclosed separately from the human reviews.

## 8:45-9:40 - Slides 17-18

The first ten displayed failures include case-specific evidence and validation follow-ups. Important limits include ambiguous spam labels, missing context in long or encoded messages, near-copy campaigns and review rules that overflag legitimate correspondence. A source-matching quote can still support weak reasoning.

The supplied complete GPU run took 194.9 seconds excluding dependency installation on RTX 4000 Ada. That is not a measured T4 runtime. CPU training/save/reload and partial CPU evidence are separately scoped. State the actual device and cache assumptions whenever discussing timing.

Our contribution is a measured triage workflow with training-only evidence, visible limitations and an explicit analyst action boundary. We are ready to discuss the masked LoRA loss, retrieval, MCP calls, failure cases and approval checks in the five-minute Q&A.

[Stop by 9:40. Use slides 19-24 only when they answer a Q&A question.]
