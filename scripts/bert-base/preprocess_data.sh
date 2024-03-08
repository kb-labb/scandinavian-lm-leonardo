# Data preprocessing for Nemo/Megatron-LM

tokenizer="KBLab/unigram-64k-pretok-small_data-tokenizer"
split="train"

echo "Preprocessing data with tokenizer $tokenizer"

# Nemo
cmd="python NeMo/scripts/nlp_language_modeling/preprocess_data_for_megatron.py \
            --input /home/fatrek/data_network/robin/data/tiny-stories/tiny-stories-train-swe.jsonl \
            --json-keys translation \
            --split-sentences \
            --tokenizer-library huggingface \
            --tokenizer-type $tokenizer \
            --output-prefix tinyswe-uni-64k-pre-$split \
            --dataset-impl mmap \
            --workers=24"

# # Megatron-LM. Needs to be patched to support HF tokenizers. See:
# # https://github.com/Lauler/Megatron-LM/tree/huggingface-tokenizer-support
# cmd="python /workspace/Megatron-LM/tools/preprocess_data.py \
#             --input tiny-stories-train-swe.jsonl \
#             --json-keys translation \
#             --split-sentences \
#             --tokenizer-name-or-path KBLab/unigram-64k-pretok-small_data-tokenizer \
#             --tokenizer-type PretrainedFromHF \
#             --output-prefix tinyswe \
#             --workers=24"

echo "Running the command $cmd"
eval $cmd
