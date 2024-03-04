#!/bin/bash

pwd

echo "inside start-training"
echo "MASTER_ADDR" $MASTER_ADDR
echo "MASTER_PORT" $MASTER_PORT
echo "NPROC_PER_NODE" $NPROC_PER_NODE
echo "SLURM_JOB_NAME" $SLURM_JOB_NAME
echo "SLURM_JOB_ID" $SLURM_JOB_ID
echo "SLURM_JOB_NODELIST" $SLURM_JOB_NODELIST
echo "SLURM_JOB_NUM_NODES" $SLURM_JOB_NUM_NODES
echo "SLURM_LOCALID" $SLURM_LOCALID
echo "SLURM_NODEID" $SLURM_NODEID
echo "SLURM_PROCID" $SLURM_PROCID
echo "SLURMD_NODENAME" $SLURMD_NODENAME

echo "WORLD_SIZE" $WORLD_SIZE
echo "RANK" $RANK
echo "NODE_RANK" $NODE_RANK
echo "GROUP_RANK" $GROUP_RANK
echo "LOCAL_RANK" $LOCAL_RANK
echo "SLURM_NODELIST" $SLURM_NODELIST
echo "SLURM_NTASKS" $SLURM_NTASKS
echo "SLURM_NTASKS_PER_NODE" $SLURM_NTASKS_PER_NODE
echo "SLURM_ARRAY_JOB_ID" $SLURM_ARRAY_JOB_ID
echo "SLURM_ARRAY_TASK_ID" $SLURM_ARRAY_TASK_ID

# export CUDA_VISIBLE_DEVICES=0,1,2,3
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"

nvidia-smi -L

# export OMP_NUM_THREADS=2

# For pytorch_2307_nemo.sif the path is: /workspace/NeMo/examples/nlp/language_modeling/megatron_bert_pretraining.py
# For nemo_2306.sif the path is: /workspace/NeMo/examples/nlp/language_modeling/megatron_bert_pretraining.py
cmd="python /workspace/nemo/examples/nlp/language_modeling/megatron_bert_pretraining.py  \
    --config-path=/leonardo_work/EUHPC_D07_027/scandinavian-lm/faton/scandinavian-lm-leonardo/configs/bert-base \
    --config-name=megatron.bert-base.unigram-64k-pretok-small_data.tinystories.config.yaml \
    "

echo "Executing Command:"
echo $cmd


$cmd