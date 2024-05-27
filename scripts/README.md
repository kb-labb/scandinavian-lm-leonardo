# Scripts

## Run Scripts

An `sbatch` launch script can either be "standalone", including all of the logic and commands to launch training within it, or it can call another bash script containing the logic to launch training. In `llama2-nanotron` and `llama2-levanter` the script is standalone, whereas in `bert-base` we use `start_script.sh` in the current directory to launch a training script in the model directory. To start BERT training with NeMo, modify `start_script.sh` to fit your needs and launch a job with:

```bash
sbatch --job-name=<my_job> scripts/start_script.sh scripts/bert-base/start_training-nemo... <user>
```

where `<my_job>` is the name of the job and `<user>` is the name of your directory in `/leonardo_work/EUHPC_D07_027/<user>`.

> [!IMPORTANT]
> Make sure your working directory (in your shell/editor) actually is an absolute path `/leonardo_work/EUHPC_D07_027/...` and not a symlink to this directory that goes through your home directory. Launching the job from a symlinked directory will cause the job to fail without any error message or logs. Type `pwd` in your terminal to check. 

See the different model subdirectories (e.g. `llama2-levanter`, `llama2-nanotron`) for detailed instructions how to launch training for those models. 

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



