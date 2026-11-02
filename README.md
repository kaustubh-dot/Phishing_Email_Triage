# Phishing email triage (P13)

A notebook project that classifies email as safe or phishing and shows the evidence behind a proposed action. It combines a Qwen LoRA classifier, MiniLM/FAISS retrieval and local indicator tools in a LangGraph workflow. Quarantine is simulated and requires an explicit analyst decision.

The complete implementation, saved outputs, evaluation and demo are in [Phishing_Email_Triage.ipynb](Phishing_Email_Triage.ipynb). Team contributions are recorded in its opening table. The repository includes both trained adapters and 30 completed human explanation ratings.

## Run locally

Use Python 3.12. Keep the notebook at the repository root so it can find the saved adapters and ratings.

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name python3
```

Open the notebook in a Jupyter-compatible editor, select `.venv/bin/python` as its kernel and run the cells in order. The first run needs internet access to download the public dataset and base models. Dependencies are pinned in `requirements.txt` and the notebook setup cell. Downloads stay in `.cache/` and are excluded from Git.

The notebook uses CUDA when available and otherwise runs on CPU. The recorded full run used an NVIDIA RTX 4000 Ada GPU. A fresh full run completed all 17 code cells in 283.5 seconds on that GPU, including kernel startup and setup. Full laptop CPU and free Colab T4 timing have not been verified.

### Run controls

- `QUICK_RUN=True` evaluates 60 fixed test emails; `False` evaluates all 300. An explicit `P13_QUICK_RUN=1` or `0` environment setting overrides the flag. The committed outputs show the full evaluation.
- `TRAIN=False` loads matching saved adapters and trains once if they are missing. `TRAIN=True` retrains both ranks. A saved adapter with mismatching metadata raises an error.
- Both modes use the same 4,000 training emails, 400 validation emails and training-only retrieval index. Seed 42, pinned dataset/model revisions and input fingerprints support reproduction.

## Results

All conditions below use the same 300 test emails: 188 safe and 112 phishing. Precision, recall and F1 treat phishing as the positive class. The notebook also reports k=1 and k=3 ablations; k=5 was selected using validation data.

| Condition | Accuracy | Precision | Recall | F1 | False-positive rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Keyword rules | 0.6433 | 0.7273 | 0.0714 | 0.1301 | 0.0160 |
| Zero-shot Qwen | 0.6267 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| MiniLM/FAISS kNN, k=5 | 0.9633 | 0.9469 | 0.9554 | 0.9511 | 0.0319 |
| LoRA rank 8 | 0.9767 | 0.9730 | 0.9643 | 0.9686 | 0.0160 |
| LoRA rank 4 | 0.9700 | 0.9813 | 0.9375 | 0.9589 | 0.0106 |
| Full defended workflow | 0.9767 | 0.9730 | 0.9643 | 0.9686 | 0.0160 |

The rank-8 classifier makes three false positives and four false negatives. The defended workflow preserves its verdict, so retrieval, tools and approval do not add a classification accuracy gain. The unchanged zero-shot model predicts every test email as safe under the notebook's constrained A/B scoring.

The full workflow produces 111 quarantine proposals, all paused for approval. Evaluation executes no quarantine. Separate integration checks cover approval, rejection, replay protection and thread isolation.

### Explanations and human ratings

Of 300 model explanations, 142 pass JSON-format and exact-quote checks; the remaining 158 use visible template fallbacks. A quote appearing in an email does not establish that the reason is correct.

The [human rating sheet](artifacts/human_explanation_ratings.csv) contains 30 completed cases. Mean ratings on a 1 to 5 scale are 4.43 for correctness, 4.37 for grounding and 3.63 for usefulness. These ratings apply to the saved email/explanation snapshot. If a rerun changes the explanations, the notebook preserves the existing sheet and creates a separate fingerprinted sheet; scores are counted only for matching text. Quick mode uses its own sheet.

### Prompt-injection test

Thirty attack pairs share ten synthetic malicious scenarios. On the same 15 pairs eligible in both defence conditions, targeted attacks succeed in 4/15 cases with defence off and 7/15 with it on. Across all 30 attacked emails, allow counts are 10/30 and 15/30. The defence does not improve this observed stress test. All attacked allow outcomes follow a safe classifier verdict, which the action-consistency rule cannot correct.

These authored cases do not establish general injection robustness. The notebook reports the individual-condition denominators, shared eligible pairs and classifier flips separately.

## Try the demo

After running the notebook, `ask(email)` prints the verdict, quoted explanation, retrieved evidence and trace, then returns a new thread ID. A proposed quarantine waits for `review(thread_id, 'approve')` or `review(thread_id, 'reject')`. Completed threads cannot be reused.

The demo includes one correctly classified held-out email and one observed failure. Complete indicators remain in graph state. Checkpoints and the simulated quarantine log are held in memory and disappear when the kernel restarts.

## Repository contents

| Path | Contents |
| --- | --- |
| `Phishing_Email_Triage.ipynb` | Implementation, evaluation, demo, team contributions, limitations and references |
| `requirements.txt` | Pinned Python dependencies |
| `artifacts/adapters/r8/` and `r4/` | Trained LoRA adapters, tokenizer files and training metadata |
| `artifacts/revisions.json` | Pinned model and dataset revisions |
| `artifacts/results/full/` | Metrics, predictions, split manifest, charts, injection cases, failure analysis and run records |
| `artifacts/human_explanation_ratings.csv` | Completed ratings for 30 saved explanations |
| `P13_Phishing_Email_Triage_Team.pdf` | Project brief |
| `0_Guidelines_and_Judging.pdf` | Assessment guidelines |

Quick results, downloaded models/data, embeddings and training checkpoints are generated locally and excluded from Git. A notebook-only copy needs the accompanying artifacts or must retrain the adapters.

## Limitations

The public dataset includes spam-like messages labelled phishing. Results describe one fixed split and do not establish performance on current threats or a statistically significant advantage over other classifiers.

One distinct safe training/test email pair becomes identical after classifier truncation. The notebook retains the original split and reports a common 299-email sensitivity check for every condition; rank-8 F1 is unchanged. Fixed input limits can also hide evidence in long emails.

Indicator tools inspect local text. They do not authenticate sender headers, visit URLs or query reputation services. The brand list is limited, and model explanations can misinterpret valid quotes. There is no live mailbox integration.

Codex assisted with implementation, experiments and notebook prose. Team members reviewed and verified the work; their contributions and the dataset, model, library and lab references are recorded in the notebook.
