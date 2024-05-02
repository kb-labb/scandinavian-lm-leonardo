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