# ToDo

## Model Todo

- Decoder models
  - [ ] Llama 1b
    - [ ] Norwegian
    - [ ] Danish
    - [ ] Swedish
  - [ ] Llama 3b
    - [ ] Norwegian
    - [ ] Danish
    - [ ] Swedish
  - [ ] Llama 8b
    - [ ] Norwegian
    - [ ] Danish
    - [ ] Swedish
- [ ] ModernBERT
  - [ ] base
    - [ ] Norwegian
    - [ ] Danish
    - [ ] Swedish
  - [ ] large
    - [ ] Norwegian
    - [ ] Danish
    - [ ] Swedish
- [x] effect of filtering on decoders
  - [x] only deduplication
  - [x] gopher rules
  - [x] educational score (1 - 5)
  - [x] askllm score (same amounts as educational score)
  - [ ] perplexity ?!

## Data Todo

- [ ] evaluate classifiers on FineWeb-c test sets
- [ ] filter datasets with perplexity ?!
- [ ] get perplexity distributions of filtered datasets ?!
- [ ] run classifiers on
  - [ ] FineWeb 2
    - [ ] Norwegian
    - [ ] Danish
    - [ ] Swedish
  - [ ] HPLT 2
    - [ ] Norwegian
    - [ ] Danish
    - [ ] Swedish
- [ ] maybe deduplicate between both

## General Todo

- [ ] conversion and continued pretraining Llama with `nanotron` works
- [ ] modernBERT
  - [ ] train
  - [ ] convert to huggingface
  - [ ] hyperparameter and training setup
- [ ] perplexity on test set for data-filtering experiments
