## Train LLama with Nanotron

Assuming you have cloned `scandinavian-lm-leonardo` and are using it as your working directory:

```bash
git clone https://github.com/huggingface/nanotron.git
```

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

Activate the virtual environment:

```bash
source venvs/nanotron-venv/bin/activate
```

### Install dependencies

First, unload the `cineca-ai` module:

```bash
module unload cineca-ai
```

Load cuda 12.1 and GCC in case they are needed for compilation:

```bash
module load cuda/12.1
module load gcc/12.2.0-cuda-12.1
```

Install the dependencies:

```bash
MAX_JOBS=6 pip install -r scripts/llama2-nanotron/requirements.txt
```

**Note**: Flash attention needs to be installed after `ninja` and `packaging` are already installed. Install it separately afterrwards with `--no-build-isolation`:

```bash
MAX_JOBS=6 pip install flash-attn --no-build-isolation
```

### Copy the tokenizer to local directory

You need to have a tokenizer saved locally, since the compute nodes don't have internet. There is an existing tokenizer in the `tokenizers` directory. You can copy it:

```bash
mkdir tokenizers
cp -r /leonardo_work/EUHPC_D07_027/tokenizers/tiny-eng-nor-swe-tokenizer tokenizers
```

Alternatively, start an interactive shell on the login node and load tokenizer from Huggingface, then save it locally:

```bash
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("organization/modelrepo")
tokenizer.save_pretrained("tokenizers/mytokenizer")
```

### Prepare the dataset

We have translated versions of the TinyStories dataset available in `/leonardo_work/EUHPC_D07_027/data`. They are in `.jsonl` format. We need to turn them into a Huggingface dataset.

Start an interactive python shell either on the login node or a compute node (if working with large very datasets): 

```bash
python
```

```python
import glob
from datasets import load_dataset
datafiles = glob.glob("/leonardo_work/EUHPC_D07_027/data/*.jsonl")
datafiles = [f for f in datafiles if "eng" not in f] # English doesn't have same columns
dataset = load_dataset("json", data_files=datafiles, cache_dir="datasets/tinystories-dataset")
```

### Model yaml config file

Check and if necessary modify the [`config_llama_7b.yaml`](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/configs/llama2-nanotron/config_llama_7b.yaml) file to point to the correct tokenizer and dataset directories. Modify `checkpoints_path` to point to a desired output directory in your working directory.

> [!NOTE]
> Adjust the data parallelism settings (`dp`) if you train on more than two nodes.

### Train the model

Launching this training job **does not** require running `start_script.sh`. We are able to launch the training with a single script. 

To train the model, you can use the `start_training.sh` script in the `scripts/llama2-nanotron` directory:

```bash
sbatch scripts/llama2-nanotron/start_training.sh
```

> [!NOTE]
> Make sure a `logs` directory exists in your workspace before starting the job.  
> Otherwise the job might crash because SLURM can't write to `logs`.

Adjust the `start_training.sh` script if necessary to point to the correct python environment (the path to activate your venv).

### Multiple epoch training

To train multiple epochs on the same data, the yaml file should be modified to repeat the dataset:

```yaml
data_stages:
- data:
    dataset:
      dataset_overwrite_cache: false
      dataset_processing_num_proc_per_process: 4
      hf_dataset_config_name: null
      hf_dataset_or_datasets: datasets/tinystories-dataset
      hf_dataset_splits: train
      text_column_name: translation
    num_loading_workers: 16
    seed: 42
  name: Stable Training Stage
  start_training_step: 1
- data:
    dataset:
      dataset_overwrite_cache: false
      dataset_processing_num_proc_per_process: 4
      hf_dataset_config_name: null
      hf_dataset_or_datasets: datasets/tinystories-dataset
      hf_dataset_splits: train
      text_column_name: translation
    num_loading_workers: 16
    seed: 42
  name: 2nd Training Stage
  start_training_step: 5000 # Figure out the correct step to start from
```
