## Scandinavian LM 

Meetings notes 

#### 2024-08-12

Discussion relating to how to best set up a dataset and relevant experiments to measure the effects of data quality filtering. The focus is to i) create a dataset from OSCAR+C4, ii) apply gopher rule-like filtering on the dataset, iii) create document quality scores, iv) train quality score classifiers.

* OSCAR and mC4 should be used as baseline datasets as opposed to CulturaX, since the latter already has had perplexity filtering applied.
* We focus on **Norwegian Bokmål** and **Swedish** in experiments to simplify the work.
* Perform Data quality filter ablations by training models on unfiltered dataset, on CulturaX (perplexity filtering), on Gopher rules + other heuristic based filters, and on classifier based filters train on the outputs of LLM doument scores.
* Candidate models to create document quality scores are **Gemma2 27B** and **Llama 3.1 70B**. The models have permissive licenses regarding the use of their outputs.
* Experiment and data filtering suggestions are summarized in [notes/experiments_data.md](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/notes/experiments_data.md).
* Suggestions on which prompts to use and evaluate, and edits to prompts are done in [notes/prompts_data.md](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/notes/prompts_data.md).
* We decided to keep meeting minutes, and add experiment suggestions in this git repo.
* Can we release the filtered corpus and how should we release it? Redistributing the original datasets with filters applied may be difficult due to licenses+legal aspects. Discussions ongoing. An alternative is to release scripts/models/hashes or other means of reproducing our dataset.
