## Nanotron Llama2 Data Experiments

```bash
git clone https://github.com/huggingface/nanotron.git
```

> [!NOTE]
> All instructions assume you are using the cloned `nanotron` repository as your working directory.

### Create python venv for the project (using `uv`)

> [!NOTE]
> Install the Python package manager `uv` on JURECA:
> `curl -LsSf https://astral.sh/uv/install.sh | sh`

Create a virtual environment:

```bash
mkdir -p venvs
uv venv venvs/nanotron --python 3.11 && source venvs/nanotron/bin/activate && uv pip install --upgrade pip
```

Install Pytorch:

```bash
uv pip install torch --index-url https://download.pytorch.org/whl/cu124
```

Install Nanotron with core dependencies:

```bash
uv pip install -e .
```

Install remaining dependencies:

```bash
uv pip install datasets transformers datatrove[io] numba wandb
```

To install Flash Attention, we first need to load the CUDA module on JURECA

```bash
module load CUDA/12
``` 

Then install flash attention with `uv`:

```bash
uv pip install ninja triton "flash-attn>=2.5.0" --no-build-isolation
```

### Data preparation

Our datasets are stored in:

* `/p/project1/jureap128/data`

And our tokenizers are stored in:

* `/p/project1/jureap128/tokenizers`

These need to be processed to [`nanoset` format](https://github.com/huggingface/nanotron/blob/main/docs/nanoset.md).

The `nanotron` library includes a script to convert the data to `nanoset` format in `tools/preprocess_data.py`. We include an sbatch script in this directory to launch a preprocessing job with the aforementioned script. See [tools/preprocess_nanoset.sh](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/scripts/llama2-data-experiments/tools/preprocess_nanoset.sh).

Adjust the paths to the `--tokenizer-name-or-path` and `--dataset` arguments to process the relevant data with the correct tokenizer.

### Training

We include an sbatch launch script for training. See `launch_train.sh` in this directory. 

Adjust the config file path to point to the correct config for your experiment.

Example configs of our data experiment ablations can be found in [configs/llama2-data-experiments](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/configs/llama2-data-experiments).

> [!TIP] 
> The `dp` (data parallel) setting needs to be set to the numebr of nodes you intend to use for training. 

> [!TIP]
> Your global batch size in terms of observatinos is going to be `micro_batch_size` * `dp` * `gradient_accumulation_steps`. To calculate your global batch size in terms of tokens, multiply this by `sequence_length`. To calculate the total number of tokens you are training over, multiply again by `train_steps`. 