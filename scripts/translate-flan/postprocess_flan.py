import argparse
import polars as pl
from datasets import load_from_disk

argparser = argparse.ArgumentParser()
argparser.add_argument("--original_dataset", type=str, default="datasets/flan_indexed")
argparser.add_argument("--language", type=str, default="swe")
args = argparser.parse_args()

dataset_name_inputs = f"datasets/flan_chunked_inputs_{args.language}_out"
dataset_name_targets = f"datasets/flan_chunked_targets_{args.language}_out"

print(f"Loading datasets {dataset_name_inputs} and {dataset_name_targets}")
dataset_original = load_from_disk(args.original_dataset)
dataset_translated_inputs = load_from_disk(dataset_name_inputs)
dataset_translated_targets = load_from_disk(dataset_name_targets)


for split in dataset_translated_inputs.keys():
    print(f"Processing {split}")
    df_translated_inputs = dataset_translated_inputs[split].to_pandas()
    df_translated_inputs = pl.DataFrame(df_translated_inputs)
    df_translated_targets = dataset_translated_targets[split].to_pandas()
    df_translated_targets = pl.DataFrame(df_translated_targets)
    df_original = dataset_original[split].to_pandas()
    df_original = pl.DataFrame(df_original)

    print("Concatenating translations")
    # Concatenate inputs_sen, translation_swe, backtranslation-swe
    df_concat_inputs = df_translated_inputs.group_by("index").agg(
        [
            pl.col("inputs_sen").str.concat(" "),
            pl.col(f"translation_{args.language}").str.concat(" "),
            pl.col(f"backtranslation_{args.language}").str.concat(" "),
        ]
    )

    df_concat_targets = df_translated_targets.group_by("index").agg(
        [
            pl.col("targets_sen").str.concat(" "),
            pl.col(f"translation_{args.language}").str.concat(" "),
            pl.col(f"backtranslation_{args.language}").str.concat(" "),
        ]
    )

    # Join with original dataset
    df_original = df_original.join(df_concat_inputs, on="index").join(
        df_concat_targets, on="index"
    )

    df_original.write_parquet(f"datasets/flan_{args.language}_{split}.parquet")
    print(f"Saved datasets/flan_{args.language}_{split}.parquet")
