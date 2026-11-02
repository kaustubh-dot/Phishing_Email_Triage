---
base_model: Qwen/Qwen2.5-0.5B-Instruct
library_name: peft
pipeline_tag: text-generation
tags:
- base_model:adapter:Qwen/Qwen2.5-0.5B-Instruct
- lora
- transformers
---

# Phishing classifier, LoRA rank 4

This adapter fine-tunes Qwen2.5-0.5B-Instruct to predict safe or phishing labels. Rank 8 is the primary classifier; rank 4 is the ablation.

Training uses 4,000 emails from `zefang-liu/phishing-email-dataset`, with 400 validation emails, seed 42 and one epoch. The adapter targets `q_proj` and `v_proj`. Exact revisions, hyperparameters and input fingerprints are in [training_metadata.json](training_metadata.json).

Phishing F1 is 0.9589 on the fixed 300-email test subset. These dataset-specific results do not establish performance on current email threats. The notebook documents truncation, input overlap and prompt-injection failures.

Run [the project notebook](../../../Phishing_Email_Triage.ipynb) for preprocessing, the A/B label prompt and saved-adapter inference. The base model is downloaded separately. This adapter is part of a notebook demonstration with simulated quarantine and analyst approval.
