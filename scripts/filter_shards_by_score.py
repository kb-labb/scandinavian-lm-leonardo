import time
import glob
import os
from argparse import ArgumentParser

import tqdm
from datasets import load_dataset

CACHE_DIR = "/leonardo_work/EUHPC_A02_045/scandinavian-lm/robin/cache_dir/"


def get_args():
    args = ArgumentParser()
    args.add_argument("--cache_dir", type=str, default="cache_dir/")
    args.add_argument("--input_dir", type=str)
    args.add_argument("--output_dir", type=str, default="outputs/")
    args.add_argument("--task", type=str, choices=["askllm", "fineweb"])
    args.add_argument("--lang", type=str, choices=["sv", "no", "da"])
    args.add_argument("--flavour", type=str, choices=["mc4", "oscar", "hplt"])
    args.add_argument("--score", type=int, default=2)

    args = args.parse_args()
    return args


def main(task, glob_string, output_dir, cache_dir, score, lang, flavour):
    if task == "fineweb":
        for fn in tqdm.tqdm(glob.glob(glob_string)):
            out_fn = output_dir + "/" + fn.split("/")[-1] + ".json"
            if os.path.isfile(out_fn):
                continue
            else:
                ds = load_dataset("parquet", data_files=fn, cache_dir=cache_dir)

                ds = ds.filter(lambda x: x["int_score"] >= score)["train"]
                ds.to_json(out_fn)

    elif task == "askllm":
        start = time.time()
        ds = load_dataset(
            "parquet",
            data_files=glob.glob(glob_string),
            cache_dir=cache_dir,
        )
        print(f"loading the data took {time.time() - start:.2f} seconds")
        start = time.time()
        ds = ds["train"]
        ds = ds.filter(lambda x: x["yes_score"] > score)
        print(ds)
        print(f"Filtering the data took {time.time() - start:.2f} seconds")
        n = len(glob.glob(glob_string))
        for i in range(n):
            start = time.time()
            out_fn = f"{output_dir}/{lang}-{flavour}-shard-{i}.json"
            ds_i = ds.shard(n, index=i)
            ds_i.to_json(out_fn)
            print(f"Writing split {i+1} of {n} took {time.time() - start:.2f} seconds")
    return

    # start = time.time()
    # ds = ds.sort("yes_score", reverse=True)["train"].select(range(size))
    # print(f"Sorting the data took {time.time() - start:.2f} seconds")
    # n = len(glob.glob(glob_string))
    # ds.save_to_disk(f"{output_dir}/{lang}-{flavour}-all")
    # return
    # for i in range(n):
    #    out_fn = f"{output_dir}/{lang}-{flavour}-shard-{i}.json"
    #    if os.path.isfile(out_fn):
    #        print(f"skip {out_fn}")
    #        continue

    #    start = time.time()
    #    ds_i = ds.shard(n, index=i)
    #    print(f"Sharding the data took {time.time() - start:.2f} seconds")
    #    start = time.time()
    #    ds_i.to_json(out_fn)
    #    print(f"Writing the data took {time.time() - start:.2f} seconds")


if __name__ == "__main__":
    args = get_args()

    """
    sv
    mc4: 34_359_510 6_849_373, 19.93%
    oscar: 4_929_358 1_181_095, 23.96%
    hplt: 12_202_742 1_503_580, 12.32%
    total: 51_491_610, 9_534_048, 18.52%
    no
    mc4: 18_023_895 2_344_543, 13.01%
    oscar: 650_821 99_102, 15.23%
    hplt: 4_426_576 351_771, 7.95%
    total: 23_101_292, 2_795_416, 12.10%
    da
    mc4: 19_842_561 2_875_732, 14.49%
    oscar: 1_664_896 332_689, 19.98%
    hplt: 3_628_347 412_363, 11.37%
    total: 25_135_804, 3_620_784, 14.40%
    """

    sizes = {
        "sv": {"mc4": 6_849_373, "oscar": 1_181_095, "hplt": 1_503_580},
        "no": {"mc4": 2_344_543, "oscar": 99_102, "hplt": 351_771},
        "da": {"mc4": 2_875_732, "oscar": 332_689, "hplt": 412_363},
    }

    thresholds = {
        "sv": 0.24368562755506545,
        "no": 0.2723624105587436,
        "da": 0.05752174956933392,
    }

    score = args.score if args.task == "fineweb" else thresholds[args.lang]
    glob_string = f"{args.input_dir}/{args.lang}-{args.flavour}-*"
    main(
        args.task,
        glob_string,
        args.output_dir,
        args.cache_dir,
        score=score,
        lang=args.lang,
        flavour=args.flavour,
    )
