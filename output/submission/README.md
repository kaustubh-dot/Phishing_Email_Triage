# Submission verification evidence

The approved reviewed notebook is published once at [Phishing_Email_Triage.ipynb](../../Phishing_Email_Triage.ipynb). This directory contains supporting evidence, not a second graded notebook.

| File or directory | Purpose |
| --- | --- |
| [source_provenance.json](source_provenance.json) | Original input hash, reviewed notebook hash, canonical published path, artifact snapshot and approval date. |
| [source_changes.diff](source_changes.diff) | Source-only comparison between the supplied notebook and reviewed version. |
| [preserved_system_sources.json](preserved_system_sources.json) | Hashes for the 15 system implementation cells preserved from the supplied notebook. |
| [original_rating_diagnostic.json](original_rating_diagnostic.json) | Reproduces the supplied rating cell's missing-file failure and historical-score mismatch. |
| [verification/full](verification/full/) | Full 300-email run, matching source hash, metrics, execution log and independent numerical checks. |
| [verification/quick](verification/quick/) | QUICK_RUN on 60 emails with verified saved assets and offline Hugging Face caches. |
| [explanation_review](explanation_review/) | All 30 historical/current pairs assessed by Codex, explicitly separate from human ratings. |

The full run completed in 203.43 seconds and quick mode in 81.16 seconds on NVIDIA RTX 4000 Ada, including the setup/kernel harness. Both executed all 21 code cells without error outputs. Installed packages and Hugging Face caches were reused; the full run downloaded and checked all 15 missing repository assets.

The [detailed assessment](../../docs/SUBMISSION_ASSESSMENT.md) describes the methodology and remaining human-rating requirement. The [results guide](../../docs/RESULTS_AND_ARCHIVE.md) and [archive index](../../archive/README.md) distinguish current, supplementary and historical evidence.
