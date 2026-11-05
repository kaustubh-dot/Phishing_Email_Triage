---
base_model: Qwen/Qwen2.5-0.5B-Instruct
library_name: peft
pipeline_tag: text-generation
tags:
- base_model:adapter:Qwen/Qwen2.5-0.5B-Instruct
- lora
- transformers
---
P13 defended rank-8 adapter. Continued label-preserving adversarial LoRA training; parent r8/r4 adapters remain unchanged. See training_metadata.json for frozen development selection and fingerprints.
### Framework versions

- PEFT 0.17.1