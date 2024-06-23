#!/bin/bash

#SBATCH --job-name=manifest   # create a short name for your job
#SBATCH --nodes=4           #161
#SBATCH --gres=gpu:4            # number of gpus per node
#SBATCH --cpus-per-task=8        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=440GB               # total memory per node 
#SBATCH --time=0-02:00:00          # total run time limit (HH:MM:SS)
#SBATCH --ntasks-per-node=4
#SBATCH --partition=boost_usr_prod
#SBATCH --qos=normal                   # long jobs
#SBATCH --account=EUHPC_D07_027
#SBATCH --output=logs/sbatch-%J.log

set -x
echo "Starting job $SLURM_JOB_ID"

SCRIPTS_DIR=/leonardo_work/EUHPC_D07_027/scandinavian-lm/faton/nemotron/scripts # Change this to your scripts directory
DATETIME=$(date +'date_%y-%m-%d_time_%H-%M-%S')
LOG_PATH="logs/${SLURM_JOB_NAME}_${DATETIME}.log"
MODEL=/leonardo_work/EUHPC_D07_027/models/Nemotron-4-340B-Instruct
CONTAINER="/leonardo_work/EUHPC_D07_027/containers/nemotron_2401.sif"
MOUNTS="${SCRIPTS_DIR}:/scripts,${MODEL}:/model,/leonardo_work/EUHPC_D07_027:/leonardo_work/EUHPC_D07_027"


CMD="bash /scripts/nemo_inference.sh /model"

echo "Running command: ${CMD}"

srun -l --output=$OUTFILE \
    singularity exec --nv --bind $MOUNTS $CONTAINER bash -c "${CMD}" 2>&1 | tee -a $LOG_PATH