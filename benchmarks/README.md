## Benchmarks

Benchmarks with throughput and token/second measurements for different libraries and models.

### Nanotron

#### LLama2 7B

Trained with `micro_batch_size=2` and `batch_accumulation_per_replica=16`. Higher gradient accumulation leads to better performance, since GPUs don't have to communicate as often. Meta trained LLama2 with a global batch size of 4 million. In comparison, our run with 32 nodes had a global batch size of `2 * 16 * 32 = 1024`. I.e. `micro_batch_size*batch_accumulation_per_replica*nodes`.  

In a larger training run we would increase the `batch_accumulation_per_replica`.

| Nodes | TFLOPs | Tokens/s  per GPU | Tokens/s |
|------:|-------:|------------------:|---------:|
| 2     |    185 |              4020 |    32200 |
| 4     |    180 |              3900 |    62400 |
| 8     |    173 |              3760 |   120000 |
| 16    |    171 |              3710 |   238000 |
| 32    |    166 |              3610 |   462000 |

### Nemo

#### BERT-base

Settings: 

* No model parallelism: `tp=1` and `pp=1`.
* `micro_batch_size=32` when training with sequence length `512`. `micro_batch_size=8` when training with sequence length `2048`.
* `global_batch_size=1024`. Divide iter/s with 4 to get estimate for 4k batch size. 

| Nodes | seqlen | Tokens/s          | Samples/s | Iter/s | Global bsz |
|------:|-------:|------------------:|----------:|-------:|-----------:|
| 2     |    512 |            597333 |     1167  |   1.18 |      1024  |
| 2     |   2048 |            413000 |      202  |   0.19 |      1024  |

Approximate compute required per 100k steps assuming `global_batch_size=4096`: 

* seqlen 512: `188 node hours` per 100k steps.
* seqlen 2048: `1151 node hours` per 100k steps. 

Compute required assuming we train **150k steps** with 512 seqlen and **50k steps** with seqlen 2048:

`1.5 * 188 + 0.5 * 1151 = 857 node hours`

#### BERT-large

Settings:

* `global_batch_size=8092`
* `tp=4` and `pp=1`
* `micro_batch_size=128`

| Nodes | seqlen | Tokens/s          | Samples/s | Iter/s | Global bsz |
|------:|-------:|------------------:|----------:|-------:|-----------:|
| 2     |    512 |            216056 |     422   | 0.0518 |       8096 |

Approximate compute required per 100k steps assuming `global_batch_size=4096`: 

* seqlen 512: `536 node hours` per 100k steps.