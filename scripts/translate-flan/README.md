## Translate FLAN

Translation scripts for translating [FLAN](https://huggingface.co/datasets/Muennighoff/flan) to Swedish using `ctranslate2`. The scripts have multi-GPU support.

> [!NOTE]
> Instructions assume this directory (`translate-flan`) is your working directory

### Environment

Load modules:

```bash
module load profile/deeplrn
module load cineca-ai/3.0.1
```

Create a virtual environment:

```bash
python -m venv venvs/translate
```

Activate the virtual environment:

```bash
source venvs/translate/bin/activate
```

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
MAX_JOBS=6 pip install -r requirements.txt
```

> [!NOTE]
> If flash attention doesn't install correctly you may have to install it outside of the requirements file with `--no-build-isolation`:

```bash
pip install flash-attn --no-build-isolation
```

### Instructions

First, download the OPUS Tatoeba MT translation models by running: 

```bash
# This should be done on login node (no internet on compute nodes)
bash download_and_convert.sh
``` 

Second, download and preprocess FLAN:

```bash
# Also on login node (internet required)
python preprocess_flan.py
```

> [!NOTE]
> The columns `inputs` and `targets` FLAN are divided into two datasets for translation.
> This is because we need to chunk the documents in order to ensure 
> 1. inference is performed the way the translation model was trained (sentence by sentence)
> 2. we do not exceed the max context length of the translation model (leading to truncation)
> Name the datasets appropriately and remember them for the next script.
> See the args in `preprocess_flan.py` for options.

Third, perform inference by running

```bash
sbatch start_training.sh
```

> [!IMPORTANT]
> The script's default parameters are set to perform translation and backtranslation for Swedish.
> It's important you adjust the args `tokenizer`, `tokenizer_backtranslation`, `model`,
> `model_backtranslation`, as well as the dataset inputs (the two datasets created by previous script).
> See `start_training.sh` for a commented out example of translating/backtranslating Norwegian.

A bash script for norwegian translation is provided in `start_training_nor.sh`:

```bash
sbatch start_training_nor.sh
```

### Combine translations

Translations need to be concatenated again and combined to a single dataset with train, validation, and test splits. This can be done by running:

```bash
python postprocess_flan.py \
    --original_dataset datasets/flan_indexed \
    --language swe

python postprocess_flan.py \
    --original_dataset datasets/flan_indexed \
    --language nor
```

### Upload to Hugging Face

To convert the dataset to a Hugging Face dataset and upload to hub, see `parquet_to_hf_dataset.py`.
