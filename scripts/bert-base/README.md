## BERT

### Container

The container `nemo_ngc_2306.sif` is uploaded to Leonardo in `/leonardo_work/EUHPC_D07_027/containers`. Point to this in your `start_script.sh` file.

### Build container

To modify or build the container from scratch see the `container` folder in this repo:

```bash
sudo singularity build nemo_ngc_2306.sif container/nemo_ngc_2306.def
```

### Data preprocessing

Assuming you have your text data in one or several `jsonl` file(s) with the following format example format:

```json
{"text": "This is a sentence.", "translation": "Detta är en mening."}
{"text": "This is another sentence.", "translation": "Detta är en annan mening."}
```

You can preprocess the data using `preprocess_data.sh`. 

The container will have the preprocessing script from Nemo/Megatron included. To start a singularity container with GPU support in interactive mode: 

```bash
singularity shell --nv nemo_ngc_2306.sif
```

Then you can run the preprocessing script (adjust paths in the script) inside the container:

```bash
bash preprocess_data.sh
```

This will produce a `.idx` and `.bin` file with the name `{prefix}_sentence.bin` and `{prefix}_sentence.idx` respectively. 

Point to `/path_to_my_data/{prefix}_sentence` in your BERT model's NeMo config file under `data_prefix`. 