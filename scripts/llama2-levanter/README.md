## Levanter

Train LLama/Mistral with [Stanford's Levanter library](https://github.com/stanford-crfm/levanter).

Levanter [documentation for getting started on GPU](https://levanter.readthedocs.io/en/latest/Getting-Started-GPU/). Follow the instructions below instead!

### Create python venv for project

Load modules:

```bash
module load profile/deeplrn
module load cineca-ai/3.0.1
```

Create venv:

```bash
virtualenv -p python3.10 venvs/levanter
source venvs/levanter/bin/activate
```

### Install dependencies

First, unload the `cineca-ai` module:

```bash
module unload cineca-ai
```

Install a version of JAX that is compatible with CUDA 12.3 and manually reinstall the `nvidia-cudnn` version to be compatible with your version of jaxlib (`pip list | grep jaxlib` should show `0.4.27+cuda12.cudnn89`):

> [!WARNING]
> JAX install `nvidia-cudnn` 9.1.0.70 by default. We need 8.9.

```bash
pip install --upgrade "jax[cuda12_local]==0.4.27" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
pip install nvidia-cudnn-cu12==8.9.7.29
```

Install Levanter in editable mode: 

```bash
git clone https://github.com/stanford-crfm/levanter.git
cd levanter
pip install -e .
```

```bash
module load cuda/12.1
module load cudnn/8.9.7.29-12--gcc--12.2.0-cuda-12.1
module load gcc/12.2.0-cuda-12.1
pip install git+https://github.com/NVIDIA/TransformerEngine.git@stable
module purge
```

### Prepare data

We converted our data to a HF dataset with a train, validation and test split. The dataset must have a field `text` containing the text of the documents. See the [docs](https://levanter.readthedocs.io/en/latest/Training-On-Your-Data/#data-format-huggingface-datasets).

If your dataset is on the Huggingface Hub and has been downloaded, or can be otherwise loaded through `load_dataset()`, training should work out of the box assuming you are pointing to the correct data directory in the config.  

However, if you used `save_to_disk()` to save your HF dataset locally, you need to patch levanter library to load data through `load_from_disk()` instead of `load_dataset()`. 

### Yaml config file

Modify the yaml config file in [configs/llama2-levanter/llama_small_fast.yaml](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/configs/llama2-levanter/llama_small_fast.yaml) to point to the directory your HF dataset is saved in. 

> [!NOTE]
> All paths in the example config file currently assume training is launched from within the git cloned Levanter library. I.e. the local tokenizer directory is also placed in there, as well as the data directory. 

### Train the model

The only necessary commands to train the model should be 

```bash
cd levanter # paths in start_training.sh and config assume we're inside cloned levanter dir
sbatch start_training.sh
```

> [!IMPORTANT]
> Make sure the logs directory specified in the `start_training.sh` script exists before starting the training. 

