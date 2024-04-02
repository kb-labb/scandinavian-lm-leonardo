import argparse
from datasets import load_dataset, load_from_disk
import sentencepiece as spm
from nltk import sent_tokenize


def encode_sen(batch, sp, column="inputs_sen"):
    """
    Tokenize the sentences
    """
    if column == "inputs_sen":
        out_dict = {
            "inputs_tokenized": sp.encode(batch[column], out_type=str),
        }
    elif column == "targets_sen":
        out_dict = {
            "targets_tokenized": sp.encode(batch[column], out_type=str),
        }
    else:
        out_dict = {"backtranslation_tokenized": sp.encode(batch[column], out_type=str)}
    return out_dict


def split_and_chunk(batch, column="inputs"):
    """
    Sentence split and create chunked dataset (1 row per sentence).
    inputs and targets have different number of sentences, we therefore
    need to handle them separately in two datasets before rejoing them later.
    """
    sentences = []
    indices = []
    for index, text in zip(batch["index"], batch[column]):
        sent_tokenized_text = sent_tokenize(text)
        sentences.extend(sent_tokenized_text)
        indices.extend([index] * len(sent_tokenized_text))

    if column == "inputs":
        return {"inputs_sen": sentences, "index": indices}
    else:
        return {"targets_sen": sentences, "index": indices}


def tokenize_column(dataset, sp, column="inputs_sen"):
    """
    Tokenize the column
    """
    dataset = dataset.map(
        encode_sen, batched=True, num_proc=6, fn_kwargs={"sp": sp, "column": column}
    )
    return dataset


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--tokenizer", type=str, default="models/eng-swe/source.spm")
    argparser.add_argument(
        "--output_inputs", type=str, default="datasets/flan_chunked_inputs_swe"
    )
    argparser.add_argument(
        "--output_targets", type=str, default="datasets/flan_chunked_targets_swe"
    )
    args = argparser.parse_args()

    # Load the dataset
    dataset = load_dataset("Muennighoff/flan", cache_dir="datasets/flan")
    # dataset = load_from_disk("datasets/flan") # If the dataset is already downloaded

    # Add index to the dataset so we can recombine the chunks later
    dataset = dataset.map(
        lambda example, idx: {"index": idx, **example},
        with_indices=True,
        num_proc=6,
        batched=True,
    )

    dataset.save_to_disk("datasets/flan_indexed")

    chunked_dataset_inputs = dataset.map(
        split_and_chunk,
        batched=True,
        num_proc=6,
        remove_columns=["inputs", "targets", "task"],
    )

    chunked_dataset_targets = dataset.map(
        split_and_chunk,
        batched=True,
        num_proc=6,
        remove_columns=["inputs", "targets", "task"],
        fn_kwargs={"column": "targets"},
    )

    sp = spm.SentencePieceProcessor(model_file=args.tokenizer)
    chunked_dataset_inputs = tokenize_column(
        chunked_dataset_inputs, sp=sp, column="inputs_sen"
    )
    chunked_dataset_targets = tokenize_column(
        chunked_dataset_targets, sp=sp, column="targets_sen"
    )

    chunked_dataset_inputs.save_to_disk(args.output_inputs)
    chunked_dataset_targets.save_to_disk(args.output_targets)
