## Nanotron Llama2 Data Experiments

```bash
git clone https://github.com/huggingface/nanotron.git
```

> [!NOTE] All instructions assume you are using the cloned `nanotron` repository as your working directory.

### Create python venv for the project

Load modules:

```bash
module load profile/deeplrn
module load cineca-ai/3.0.1
```

Create a virtual environment:

```bash
python -m venv venvs/nanotron-venv
```

### Install dependencies

First, unload the `cineca-ai` module:

```bash
module unload cineca-ai
```

Activate the virtual environment and install the dependencies from the `nanotron` folder (see the `requirements.txt` file included in this directory):

```bash
source venvs/nanotron-venv/bin/activate
```

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> [!IMPORTANT] The line `--editable .[nanosets]` in `requirements.txt` assumes you are in the `nanotron` directory when installing. Either navigate to the `nanotron` directory or edit the line to provide a relative path to the `nanotron` directory from your current terminal location.

**Note**: Flash attention needs to be installed after `ninja` and `packaging` are already installed. Install it separately afterwards with `--no-build-isolation`:

```bash
MAX_JOBS=6 pip install flash-attn --no-build-isolation
```

### Data preparation

Our datasets are stored in:

* **Deduplicated Gopher** preprocessed data: `/leonardo_work/EUHPC_A02_045/data/dedup-doc-url-gopher/jsonl`
* **Fineweb filtered data**:  `/leonardo_work/EUHPC_A02_045/data/llm_filtered/fineweb-70b-bert-2`
* **Ask-LLM filtered data**:  `/leonardo_work/EUHPC_A02_045/data/llm_filtered/askllm`

And our tokenizers for the respective languages are stored in:

* `/leonardo_work/EUHPC_A02_045/tokenizers/tokenizer-nanotron-ablations`

These need to be processed to [`nanoset` format](https://github.com/huggingface/nanotron/blob/main/docs/nanoset.md).

The `nanotron` library includes a script to convert the data to `nanoset` format in `tools/preprocess_data.py`. We include an sbatch script in this directory to launch a preprocessing job with the aforementioned script. See [tools/preprocess_nanoset.sh](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/scripts/llama2-data-experiments/tools/preprocess_nanoset.sh).

Adjust the paths to the `--tokenizer-name-or-path` and `--dataset` arguments to process the relevant data with the correct tokenizer.

### Training

We include an sbatch launch script for training. See `launch_train.sh` in this directory. 

Adjust the config file path to point to the correct config for your experiment.

Example configs of our data experiment ablations can be found in [configs/llama2-data-experiments](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/configs/llama2-data-experiments).

> [!TIP] The `dp` (data parallel) setting needs to be set to the numebr of nodes you intend to use for training. 

> [!TIP] Your global batch size in terms of observatinos is going to be `micro_batch_size` * `dp` * `gradient_accumulation_steps`. To calculate your global batch size in terms of tokens, multiply this by `sequence_length`. To calculate the total number of tokens you are training over, multiply again by `train_steps`. 