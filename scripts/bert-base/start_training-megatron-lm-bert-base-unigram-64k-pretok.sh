#!/bin/bash

export CUDA_DEVICE_MAX_CONNECTIONS=1

# Change for multinode config
# MASTER_ADDR=localhost
# MASTER_PORT=15524
WORLD_SIZE=$(($SLURM_JOB_NUM_NODES*$NPROC_PER_NODE))

CHECKPOINT_PATH=checkpoints
DATA_PATH=/leonardo_work/EUHPC_D07_027/data/swedish/uni-64k-pretok/tinyswe-uni-64k-pre-train_translation_sentence

DISTRIBUTED_ARGS="--nproc_per_node $NPROC_PER_NODE \
                  --nnodes $SLURM_JOB_NUM_NODES \
                  --node_rank $SLURM_NODEID \
                  --master_addr $MASTER_ADDR \
                  --master_port $MASTER_PORT"

BERT_ARGS="
    --num-layers 24 \
    --hidden-size 1024 \
    --num-attention-heads 16 \
    --seq-length 512 \
    --max-position-embeddings 512 \
    --micro-batch-size 4 \
    --global-batch-size 32 \
    --lr 0.0001 \
    --train-iters 1000000 \
    --lr-decay-iters 990000 \
    --lr-decay-style linear \
    --min-lr 1.0e-5 \
    --weight-decay 1e-2 \
    --lr-warmup-fraction .01 \
    --clip-grad 1.0 \
    --fp16
"

DATA_ARGS="
    --data-path $DATA_PATH \
    --tokenizer-name-or-path KBLab/unigram-64k-pretok-small_data-tokenizer \
    --tokenizer-type PretrainedFromHF \
    --data-impl mmap \
    --split 949,50,1
"

OUTPUT_ARGS="
    --log-interval 100 \
    --save-interval 10000 \
    --eval-interval 1000 \
    --eval-iters 10
"

torchrun $DISTRIBUTED_ARGS /workspace/Megatron-LM/pretrain_bert.py \
    --use-flash-attn \
    $BERT_ARGS \
    $DATA_ARGS \
    $OUTPUT_ARGS \
    --distributed-backend nccl \
    --save $CHECKPOINT_PATH \
    --load $CHECKPOINT_PATH