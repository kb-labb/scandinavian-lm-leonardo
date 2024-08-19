## Data quality experiments

Suggested experiments to run to measure the effects of data quality filtering.

### Data

* **OSCAR** and **C4** are used as baseline dataset (since CulturaX already has perplexity filtering applied on top of these).
* **Swedish** and **Norwegian Bokmål** are used for data experiments.

#### Filters to apply

* None (use baseline datasets, OSCAR+C4)
* Deduplication
* CulturaX (use CulturaX dataset, and compare results to our Gopher rules and heuristics)
* Gopher rules and other heuristic based filters (applied on top of OSCAR+C4)
* Document quality classifier filter:
  a. Educational value score
  b. Cleanness score

#### Experimental setting

* Ablation study training models on all levels of filtering. 
* Models of a given size should be trained the same amount of steps (processing the same amount of tokens) for a fair comparison.
* Repeat data for filtered datasets (if necessary)?

#### Experiments to run (models)

Options:

* BERT-base models.
* Pretrain from scratch: "Smaller" GPT/LLama-like models (1B, 1.7B).
* Start from existing LLama checkpoint (1.7B or smaller): [SmolLM](https://huggingface.co/HuggingFaceTB/SmolLM-1.7B).
* Continue pretraining on Llama-8B for fewer tokens (one month of compute is 220B tokens worth of experiments in terms of throughput).

#### Evaluation

Evaluate scores throughout training like [Fineweb Edu](https://huggingface.co/spaces/HuggingFaceFW/blogpost-fineweb-v1). Benchmark on:

* Selected benchmarks from ScandEval.
* [SuperLim](https://github.com/spraakbanken/SuperLim-2)
* [NorBench](https://github.com/ltgoslo/norbench)
