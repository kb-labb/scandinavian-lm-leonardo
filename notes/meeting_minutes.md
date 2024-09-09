## Scandinavian LM 

Meetings notes 

#### 2024-09-09

Discussions relating to quality scoring with LLMs. Previous 2 weeks we scores 500k docs each in Swedish, Norwegian and Danish with the original fineweb prompt (in English). This week we want to add the original Ask-LLM prompt for comparison. Additionally, train BERT regressors on the fineweb scores so we can score the entire corpus with fineweb-edu scores.

* Score the already annotated docs with Ask-LLM too. Calculate correlation and create confusion matrices comparing vs fineweb-edu scores.
* Score the entire corpus with Ask-LLM (the version of corpora where dedup+Gopher rules have been applied).
* Score subset of already annotated docs with alternative fineweb-edu prompts (in Swedish, Norwegian). Correlation and confusion matrices vs original prompts.
* Apply and add fineweb prompt in English to [evaluation dataset](https://huggingface.co/datasets/ScandLM/eval_educational_prompt) of manually annotated good/bad examples, so we can compare against prompts written in Swedish and Norwegian.
* Upload documents score with fineweb-edu to HF.
* Train BERT regressors on fineweb-edu output.

#### 2024-08-19

During the previous week we debugged Gopher rules for data preprocessing, since the rules were unexpectedly removing too much data. The plan this week is to transfer data to the HPC and create document quality scores and train quality score classifiers. We also discussed whether to perform experiments where we i) pretrain 1.7B Llama models from scratch, ii) start from existing (SmolLM) checkpoint, iii) continue pretraining on Llama-8B, or iv) train BERTs.

* Need to decide on an English dataset to use when doing continued pretraining (and maybe also experiments). Fineweb Edu?
* Add a code dataset ([The Stack v2](https://huggingface.co/collections/bigcode/starcoder2-65de6da6e87db3383572be1a)).
* Suggestion ot create a LLM scorer that filters and upweights for documents with cultural/language specific knowledge of Scandinavian.

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
