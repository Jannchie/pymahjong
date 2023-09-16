# %%
import os
from core.generator import generate_sorted_seqs_set
from core.syanten import syanten
import gzip
from tqdm import tqdm
import pickle


def generate_syanten_dict(seqs_data: list):
    syanten_dict = {}
    for seq in tqdm(seqs_data):
        syanten_dict[seq] = syanten(seq)
    return syanten_dict


if os.path.exists("./data/seqs.pkl.gz"):
    print("Loading seqs.pkl.gz")
    seqs_data = pickle.loads(gzip.open("./data/seqs.pkl.gz", "rb").read())
else:
    seqs_data = generate_sorted_seqs_set()
    gzip.open("./data/seqs.pkl.gz", "wb").write(pickle.dumps(seqs_data))
# %%


def save_dict(syanten_dict: dict):
    gzip.open("./data/syanten_dict.pkl.gz", "wb").write(pickle.dumps(syanten_dict))


save_dict(generate_syanten_dict(seqs_data))
