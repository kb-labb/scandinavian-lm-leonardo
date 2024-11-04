#!/bin/bash

#SBATCH --job-name=nano_2b_sv   # create a short name for your job
#SBATCH --nodes=4           #161
#SBATCH --gres=gpu:4            # number of gpus per node
#SBATCH --cpus-per-task=32        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=400GB               # total memory per node 
#SBATCH --time=1-00:00:00          # total run time limit (HH:MM:SS)
#SBATCH --ntasks-per-node=1
#SBATCH --partition=boost_usr_prod
#SBATCH --qos=normal                   #default
#SBATCH --account=EUHPC_A02_045
#SBATCH --exclude=lrdn[2000-3500]
#SBATCH --output=logs/sbatch-%J.log

module purge

# Python venv path to activate. Edit if needed
VENV_ACTIVATE_PATH="venvs/nanotron-venv/bin/activate"
source $VENV_ACTIVATE_PATH
echo "Python path: " $(which python)

export CUDA_DEVICE_MAX_CONNECTIONS=1 # Important for Nanotron
export OMP_NUM_THREADS=2

# EDIT if it's not 8-gpus per node
GPUS_PER_NODE=4
NNODES=$SLURM_NNODES

# define the node 0 hostname:port
MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
MASTER_PORT=25678
echo "Master addr: $MASTER_ADDR:$MASTER_PORT"

LAUNCHER="python -u -m torch.distributed.run \
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --node_rank \$SLURM_PROCID \
    --rdzv_id $SLURM_JOB_ID \
    --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \
    --rdzv_backend c10d \
    --max_restarts 0 \
    --role \$(hostname -s|tr -dc '0-9'): \
    --tee 3 \
    "

# Check that relative paths to your `run_train.py` are correct
PROGRAM="run_train.py --config-file configs/llama2-nanotron/config_llama_2b_sv.yaml"

export CMD="${LAUNCHER} ${PROGRAM}"

echo $CMD

# EDIT: useful for debug if needed
#
# to debug NCCL issues
# export NCCL_DEBUG=INFO
#
# to unravel async errors w/o the correct traceback - potentially makes everything very slower
# export CUDA_LAUNCH_BLOCKING=1
#
# to force crashing on nccl issues like hanging broadcast
# export NCCL_ASYNC_ERROR_HANDLING=1


# srun error handling:
# --wait=60: wait 60 sec after the first task terminates before terminating all remaining tasks
# --kill-on-bad-exit=1: terminate a step if any task exits with a non-zero exit code
SRUN_ARGS=" \
    --wait=60 \
    --kill-on-bad-exit=1 \
    --jobid $SLURM_JOB_ID \
    "

DATETIME=$(date +'date_%y-%m-%d_time_%H-%M-%S')
LOG_PATH="logs/${SLURM_JOB_NAME}_${DATETIME}.log"

# bash -c is needed for the delayed interpolation of env vars to work
srun $SRUN_ARGS bash -c "$CMD" 2>&1 | tee -a $LOG_PATH