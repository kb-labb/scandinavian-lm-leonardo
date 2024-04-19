import argparse
import logging
from functools import partial
import torch
from datasets import load_from_disk
import ctranslate2
import sentencepiece as spm
from tqdm import tqdm
from preprocess_flan import tokenize_column


logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# Custom collator that allows variable length inputs
def collate_fn(batch, column="inputs_tokenized"):
    batch = [x[column] for x in batch if x is not None]
    return batch


def decode_batch(results):
    decoded_sentences = []
    for result in results:
        decoded_sentences.append("".join(result.hypotheses[0]).replace("▁", " ").strip())
    return decoded_sentences


def predict(model, split, dataset, tokenized_column, num_workers=8):
    dataloader = torch.utils.data.DataLoader(
        dataset=dataset[split],
        batch_size=8192,
        collate_fn=partial(collate_fn, column=tokenized_column),
        num_workers=num_workers,
    )
    decoded_outputs = []

    for batch in tqdm(dataloader):
        results = model.translate_batch(
            batch, max_batch_size=256, max_input_length=1524, max_decoding_length=1024
        )
        decoded_outputs.extend(decode_batch(results))

    return decoded_outputs


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--model", type=str, default="models/ct2/eng-swe")
    argparser.add_argument("--model_backtranslate", type=str, default="models/ct2/swe-eng")
    argparser.add_argument("--tokenizer", type=str, default="models/eng-swe/source.spm")
    argparser.add_argument(
        "--tokenizer_backtranslate", type=str, default="models/swe-eng/source.spm"
    )
    argparser.add_argument(
        "--splits", type=str, default=["train", "validation", "test"], nargs="+"
    )
    argparser.add_argument(
        "--inputs_dataset",
        type=str,
        default="datasets/flan_chunked_inputs_swe",
        help="Inputs from FLAN to be translated.",
    )
    argparser.add_argument(
        "--targets_dataset",
        type=str,
        default="datasets/flan_chunked_targets_swe",
        help="Targets from FLAN to be translated.",
    )
    argparser.add_argument("--output_inputs", type=str, default="datasets/flan_chunked_inputs_swe")
    argparser.add_argument(
        "--output_targets", type=str, default="datasets/flan_chunked_targets_swe"
    )
    argparser.add_argument("--backtranslate", action="store_true")
    args = argparser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    # Load the dataset
    chunked_dataset_inputs = load_from_disk(args.inputs_dataset)
    chunked_dataset_targets = load_from_disk(args.targets_dataset)

    sp = spm.SentencePieceProcessor(model_file=args.tokenizer)

    devices = list(range(torch.cuda.device_count()))
    translator = ctranslate2.Translator(args.model, device="cuda", device_index=devices)
    column_name_translate = "translation_swe" if "swe" in args.model else "translation_nor"

    logger.info(f"Translating the dataset to column {column_name_translate}.")
    # Translate the inputs
    for split in args.splits:
        # Translate the inputs
        decoded_outputs = predict(
            translator,
            split,
            chunked_dataset_inputs,
            tokenized_column="inputs_tokenized",
            num_workers=12,
        )
        chunked_dataset_inputs[split] = chunked_dataset_inputs[split].add_column(
            column_name_translate, decoded_outputs
        )

        # Translate the targets
        decoded_outputs = predict(
            translator,
            split,
            chunked_dataset_targets,
            tokenized_column="targets_tokenized",
            num_workers=12,
        )
        chunked_dataset_targets[split] = chunked_dataset_targets[split].add_column(
            column_name_translate, decoded_outputs
        )

    logger.info(
        f"Translation complete. {column_name_translate} column added to {chunked_dataset_inputs} and {chunked_dataset_targets}."
    )
    column_name_backtranslate = (
        "backtranslation_swe" if "swe" in args.model else "backtranslation_nor"
    )

    logger.info(f"Backtranslating the dataset to column {column_name_backtranslate}.")
    if args.backtranslate:
        sp = spm.SentencePieceProcessor(model_file=args.tokenizer_backtranslate)
        translator = ctranslate2.Translator(
            args.model_backtranslate, device="cuda", device_index=devices
        )

        # Tokenize the newly translated columns to prepare for backtranslation
        chunked_dataset_inputs = tokenize_column(
            chunked_dataset_inputs, sp=sp, column=column_name_translate
        )
        chunked_dataset_targets = tokenize_column(
            chunked_dataset_targets, sp=sp, column=column_name_translate
        )

        for split in args.splits:
            decoded_outputs = predict(
                translator,
                split,
                chunked_dataset_inputs,
                tokenized_column="backtranslation_tokenized",
                num_workers=12,
            )
            chunked_dataset_inputs[split] = chunked_dataset_inputs[split].add_column(
                column_name_backtranslate, decoded_outputs
            )

            decoded_outputs = predict(
                translator,
                split,
                chunked_dataset_targets,
                tokenized_column="backtranslation_tokenized",
                num_workers=12,
            )
            chunked_dataset_targets[split] = chunked_dataset_targets[split].add_column(
                column_name_backtranslate, decoded_outputs
            )

    logger.info(
        f"Backtranslation complete. {column_name_backtranslate} column added to {chunked_dataset_inputs} and {chunked_dataset_targets}."
    )
    # Save the dataset
    chunked_dataset_inputs.save_to_disk(args.output_inputs)
    chunked_dataset_targets.save_to_disk(args.output_targets)
