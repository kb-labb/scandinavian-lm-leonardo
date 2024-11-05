import json
from datasets import load_dataset
import glob
import argparse
import random

CACHE_DIR = "/leonardo_work/EUHPC_A02_045/scandinavian-lm/robin/cache_dir/"


def load_data(glob_expression):
    fns = glob.glob(glob_expression)
    print(glob_expression)
    print(fns)
    ds = load_dataset("json", data_files=fns, cache_dir=CACHE_DIR)

    return ds


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--dedup")
    parser.add_argument("--gopher")
    parser.add_argument("--fineweb")
    parser.add_argument("--askllm")
    parser.add_argument("--outfile")

    return parser.parse_args()


def main(args):
    print(args)

    sample_n = 1_000

    ds_dedup = load_data(args.dedup)
    ids_dedup = set(ds_dedup["train"]["id"])
    print(f"#docs dedup: {len(ds_dedup['train'])}")

    ds_gopher = load_data(args.gopher)
    ids_gopher = set(ds_gopher["train"]["id"])
    print(f"#docs gopher: {len(ds_gopher['train'])}")

    ids_dedup_not_gopher = ids_dedup - ids_gopher
    if not ids_dedup_not_gopher:
        ids_dedup_not_gopher = ids_dedup
    print(f"#docs dedup not gopher: {len(ids_dedup_not_gopher)}")
    sampled_ids_dedup = random.choices(
        list(ids_dedup_not_gopher), k=len(ids_dedup) // sample_n
    )
    seen = set(sampled_ids_dedup)
    sampled_ids_gopher = random.choices(
        list(ids_gopher - seen), k=len(ids_gopher) // sample_n
    )
    seen = seen.union(set(sampled_ids_gopher))

    ds_fw = load_data(args.fineweb)
    ids_fw = set(ds_fw["train"]["id"])
    print(f"#docs fineweb: {len(ds_fw['train'])}")

    ds_ask = load_data(args.askllm)
    ids_ask = set(ds_ask["train"]["id"])
    print(f"#docs askllm: {len(ds_ask['train'])}")

    ids_fw_not_ask = ids_fw.difference(ids_ask)
    ids_ask_not_fw = ids_ask.difference(ids_fw)

    print(
        len(ids_fw.difference(ids_ask)),
        len(ids_fw.union(ids_ask)),
        len(ids_fw.intersection(ids_ask)),
    )
    print(
        len(ids_ask.difference(ids_fw)),
        len(ids_ask.union(ids_fw)),
        len(ids_ask.intersection(ids_fw)),
    )

    print(f"#docs finweb without askllm {len(ids_fw_not_ask)}")
    print(f"#docs askllm without fineweb {len(ids_ask_not_fw)}")

    ids_fw_ask = ids_fw.union(ids_ask)
    sampled_ids_fw_ask = random.choices(
        list(ids_fw_ask - seen), k=len(ids_fw_ask) // sample_n
    )

    sampled_ids_fw_not_ask = random.choices(
        [x for x in ids_fw_not_ask if x not in sampled_ids_fw_ask and x not in seen],
        k=len(ids_fw_not_ask) // sample_n,
    )
    sampled_ids_ask_not_fw = random.choices(
        [x for x in ids_ask_not_fw if x not in sampled_ids_fw_ask and x not in seen],
        k=len(ids_ask_not_fw) // sample_n,
    )

    d = {
        "dedup": sampled_ids_dedup,
        "gopher": sampled_ids_gopher,
        "fineweb+askllm": sampled_ids_fw_ask,
        "fineweb-only": sampled_ids_fw_not_ask,
        "askllm-only": sampled_ids_ask_not_fw,
    }

    with open(args.outfile, "w") as fout:
        json.dump(d, fout)


if __name__ == "__main__":
    main(get_args())
