# Scripts

## Run Scripts

See `start_script.sh` for a template of how to launch jobs on Leonardo with `sbatch`. Modify the script to fit your needs and launch a job with:

```bash
sbatch start_script.sh --job-name=<my_job> bert-base/start_training.sh <user>
```

where `<my_job>` is the name of the job and `<user>` is the name of your directory in `/leonardo_work/EUHPC_D07_027/<user>`.

See the different model folders (e.g. `bert-base`) for examples of training launch scripts.

## Data preprocessing

See each model folder for data preprocessing scripts for the respective model and description of how to use them. 

## Other

### `translate_ctranslate2.py`

Little script used to translate the "Tiny Stories" dataset to Swedish and
Norwegian.


- Install `ctranslate2` via `pip install ctranslate2`.
- Choose and download the model here:
  (https://github.com/Helsinki-NLP/Tatoeba-Challenge/tree/master/models)
- Unzip `unzip opus+bt-2021-04-20.zip -d eng-nor`
- Convert the models `ct2-opus-mt-converter --model_dir eng-nor --output_dir
  eng-nor-ct2`
- run script



