# Submission verification evidence

The approved reviewed notebook is published once at [Phishing_Email_Triage.ipynb](../../Phishing_Email_Triage.ipynb). This directory contains supporting evidence, not a second graded notebook.

| File or directory | Purpose |
| --- | --- |
| [source_provenance.json](source_provenance.json) | Original input and reviewed notebook hashes, current notebook hashes, canonical published path, artifact snapshot, approval date and attribution cleanup scope. |
| [source_changes.diff](source_changes.diff) | Historical source-only comparison between the supplied notebook and reviewed version, with attribution wording normalized. |
| [preserved_system_sources.json](preserved_system_sources.json) | Historical hashes for the 15 system implementation cells preserved in the pre-cleanup reviewed notebook. |
| [original_rating_diagnostic.json](original_rating_diagnostic.json) | Reproduces the supplied rating cell's missing-file failure and historical-score mismatch. |
| [verification/full](verification/full/) | Full 300-email run, pre-cleanup source hash, metrics, execution log and independent numerical checks. |
| [verification/quick](verification/quick/) | QUICK_RUN on 60 emails with the pre-cleanup source hash, verified saved assets and offline Hugging Face caches. |
| [explanation_review](explanation_review/) | Diagnostic assessment of all 30 historical/current pairs, separate from the required rating sheet. |

The full run completed in 203.43 seconds and quick mode in 81.16 seconds on NVIDIA RTX 4000 Ada, including the setup/kernel harness. Both executed all 21 code cells without error outputs. Installed packages and Hugging Face caches were reused; the full run downloaded and checked all 15 missing repository assets.

The subsequent attribution cleanup changes commentary, diagnostic labels and supplementary assessment column names. Execution-log headings and historical diff wording are normalized as well. Original execution hashes remain preserved; this cleanup does not claim a new inference run or additional completed ratings.

The [detailed assessment](../../docs/SUBMISSION_ASSESSMENT.md) describes the methodology and remaining human-rating requirement. The [results guide](../../docs/RESULTS_AND_ARCHIVE.md) and [archive index](../../archive/README.md) distinguish current, supplementary and historical evidence.
