#!/bin/bash

#SBATCH --job-name=translate_nor   # create a short name for your job
#SBATCH --nodes=1           #161
#SBATCH --gres=gpu:4            # number of gpus per node
#SBATCH --cpus-per-task=18        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=312GB               # total memory per node 
#SBATCH --time=2-00:00:00          # total run time limit (HH:MM:SS)
#SBATCH --ntasks-per-node=1
#SBATCH --partition=boost_usr_prod
#SBATCH --qos=boost_qos_lprod                  #default
#SBATCH --account=EUHPC_D07_027
#SBATCH --output=logs/sbatch-%J.log

module purge

# Python venv path to activate. Edit if needed
VENV_ACTIVATE_PATH="venvs/translate/bin/activate"
source $VENV_ACTIVATE_PATH
echo "Python path: " $(which python)

export CUDA_DEVICE_MAX_CONNECTIONS=1 # Important for Nanotron
export OMP_NUM_THREADS=16

MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
echo "Master addr: $MASTER_ADDR:$MASTER_PORT"

# Output dataset name needs to be different from input dataset
# because arrow tables are immutable (can't overwrite)
CMD="python translate_flan.py \
    --model models/ct2/eng-nor \
    --model_backtranslate models/ct2/nor-eng \
    --tokenizer models/eng-nor/source.spm \
    --tokenizer_backtranslate models/nor-eng/source.spm \
    --inputs_dataset datasets/flan_chunked_inputs_nor \
    --targets_dataset datasets/flan_chunked_targets_nor \
    --output_inputs datasets/flan_chunked_inputs_nor_out \
    --output_targets datasets/flan_chunked_targets_nor_out \
    --backtranslate \
    "

SRUN_ARGS=" \
    --wait=60 \
    --kill-on-bad-exit=1 \
    --jobid $SLURM_JOB_ID \
    "

DATETIME=$(date +'date_%y-%m-%d_time_%H-%M-%S')
LOG_PATH="logs/${SLURM_JOB_NAME}_${DATETIME}.log"

srun $SRUN_ARGS bash -c "$CMD" 2>&1 | tee -a $LOG_PATH
