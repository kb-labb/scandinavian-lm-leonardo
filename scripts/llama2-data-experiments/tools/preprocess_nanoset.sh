#!/bin/bash

#SBATCH --job-name=nset   # create a short name for your job
#SBATCH --nodes=1           #161
#SBATCH --gres=gpu:1            # number of gpus per node
#SBATCH --cpus-per-task=32        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=460GB               # total memory per node 
#SBATCH --time=0-02:10:00          # total run time limit (HH:MM:SS)
#SBATCH --ntasks-per-node=1
#SBATCH --partition=boost_usr_prod
#SBATCH --qos=normal                   #default
#SBATCH --account=EUHPC_A02_045
#SBATCH --output=logs/sbatch-%J.log

module purge

export OMP_NUM_THREADS=1

# Python venv path to activate. Edit if needed
VENV_ACTIVATE_PATH="venvs/nanotron-venv/bin/activate"
source $VENV_ACTIVATE_PATH
echo "Python path: " $(which python)

LANGUAGE="da"

# /leonardo_work/EUHPC_A02_045/models/Meta-Llama-3.1-8B
python tools/preprocess_data.py \
       --tokenizer-name-or-path /leonardo_work/EUHPC_A02_045/scandinavian-lm/faton/nanotron/tokenizer/${LANGUAGE}/tokenizer.json \
       --output-folder datasets/nanoset-fineweb-70b-2/${LANGUAGE}_eos \
       --n-tasks 25 \
       --eos-token "</s>" \
       jsonl \
       --dataset data/fineweb-70b-2/${LANGUAGE}