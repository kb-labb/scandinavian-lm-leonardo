#!/bin/bash
#SBATCH --job-name=levanter-test
#SBATCH --nodes=4
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=8
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64G
#SBATCH --partition=boost_usr_prod
#SBATCH --qos=normal                   #default
#SBATCH --account=EUHPC_D07_027
#SBATCH --output=logs/sbatch-levanter_%J.log

mkdir -p logs

# module purge
# module load singularity

## On the Stanford NLP cluster you might need this:
# export PATH=$(echo $PATH | sed 's|:/usr/local/cuda/bin||')

# Python venv path to activate. Edit if needed
VENV_ACTIVATE_PATH="venvs/levanter/bin/activate"
source $VENV_ACTIVATE_PATH
echo "Python path: " $(which python)

# export CUDA_DEVICE_MAX_CONNECTIONS=1 # Important for Nanotron
# export OMP_NUM_THREADS=16

CMD="python -m levanter.main.train_lm \
    --config config/llama_small_fast.yaml \
    --trainer.per_device_parallelism -1 \
    --trainer.ray.auto_start_cluster false
    "

# srun error handling:
# --wait=60: wait 60 sec after the first task terminates before terminating all remaining tasks
# --kill-on-bad-exit=1: terminate a step if any task exits with a non-zero exit code
SRUN_ARGS=" \
    --wait=60 \
    --kill-on-bad-exit=1 \
    --jobid $SLURM_JOB_ID \
    "

DATETIME=$(date +'date_%y-%m-%d_time_%H-%M-%S')
LOG_PATH="../logs/${SLURM_JOB_NAME}_${DATETIME}.log"

cd levanter
srun $SRUN_ARGS bash -c "$CMD" 2>&1 | tee -a $LOG_PATH
