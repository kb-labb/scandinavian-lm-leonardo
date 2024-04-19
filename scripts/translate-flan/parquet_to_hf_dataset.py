from datasets import load_dataset
from pprint import pprint

# Load dataset splits from different parquet files
dataset = load_dataset(
    "parquet",
    data_files={
        "train": "datasets/flan_swe_train.parquet",
        "validation": "datasets/flan_swe_validation.parquet",
        "test": "datasets/flan_swe_test.parquet",
    },
    cache_dir="datasets/cache",
)

dataset = dataset.remove_columns(["inputs_sen", "targets_sen"])
dataset = dataset.rename_columns(
    {
        "translation_swe": "inputs_swe",
        "translation_swe_right": "targets_swe",
        "backtranslation_swe": "inputs_backtranslation",
        "backtranslation_swe_right": "targets_backtranslation",
    }
)

dataset_nor = load_dataset(
    "parquet",
    data_files={
        "train": "datasets/flan_nor_train.parquet",
        "validation": "datasets/flan_nor_validation.parquet",
        "test": "datasets/flan_nor_test.parquet",
    },
    cache_dir="datasets/cache",
)

dataset_nor = dataset_nor.remove_columns(["inputs_sen", "targets_sen"])
dataset_nor = dataset_nor.rename_columns(
    {
        "translation_nor": "inputs_nor",
        "translation_nor_right": "targets_nor",
        "backtranslation_nor": "inputs_backtranslation",
        "backtranslation_nor_right": "targets_backtranslation",
    }
)

# Sort dataset according to index
dataset = dataset.sort("index")
dataset_nor = dataset_nor.sort("index")


dataset.push_to_hub("Lauler/flan-swedish")
dataset_nor.push_to_hub("Lauler/flan-norwegian")
