import ctranslate2
import sentencepiece as spm
import sys
from datasets import load_dataset
from time import time
import json
from tqdm import tqdm
import os


dataset = load_dataset("roneneldan/TinyStories", cache_dir="/home/.cache/huggingface/datasets")

model = sys.argv[1]
fn_out = sys.argv[2]

meta_character = "▁"

sp = spm.SentencePieceProcessor()
sp.load(f"{model}/source.spm")
translator = ctranslate2.Translator(f"{model}-ct2",
                                    device="cuda",
                                    # num_active_batches=32,
                                    # num_queued_batches=32,
                                    compute_type="int8",
                                    # inter_threads=4,
                                   )

# source = sp.encode(["Mary had a little lamb and led it to the slaughter."], out_type=str)

batch_size = 1024
if os.path.isfile(fn_out):
    yes_no = input(f"{fn_out} exists? Do you want to delete it and continue? y/n")
    if yes_no == "y":
        os.remove(fn_out)
    else:
        exit()

dataset = dataset["validation"]["text"]

for pos in tqdm(range(0, len(dataset), batch_size)):
    print("start encoding")
    start = time()
    source = sp.encode(dataset[pos:pos + batch_size], out_type=str)
    print(f"encoding took {time() - start:.4f}s")
    
    print(f"filtering docs greater than 500")
    start = time()
    _source = filter(lambda x: len(x[1]) < 500, enumerate(source))
    ids, source = zip(*_source)
    ids = [i+pos for i in ids]
    print(f"length of filtered dataset {len(source)}")
    print(f"filtering took {time() - start:.4f}s")

    # source_batch = source[pos:pos + batch_size]
    # ids_batch = ids[pos:pos + batch_size]

    print("start translating")
    start = time()
    results = translator.translate_batch(source, max_batch_size=64)
    print(f"translating took {time() - start:.4f}s")
    
    print("start decoding")
    start = time()
    with open(fn_out, "a") as fout:
            output = [x.replace(meta_character, " ") for x in sp.decode([r.hypotheses[0] for r in results])]
            for i, o in zip(ids, output):
                print(json.dumps({"id": i, "translation": o}), file=fout)
                
    print(f"decoding took {time() - start:.4f}s")
