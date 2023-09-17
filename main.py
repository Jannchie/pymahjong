# %%
import multiprocessing
import os
from core.generator import generate_seqs_set
from core.syanten import syanten
import gzip
from tqdm import tqdm
import pickle


def calculate_syanten(seq):
    return (seq, syanten(seq))


def syanten_dict(seqs_data: list):
    if os.path.exists("./data/syanten.pkl.gz"):
        return pickle.loads(gzip.open("./data/syanten.pkl.gz", "rb").read())
    # 使用多进程池
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # 并行计算syanten
    results = list(tqdm(pool.imap(calculate_syanten, seqs_data), total=len(seqs_data)))

    # 关闭进程池
    pool.close()
    pool.join()

    # 创建syanten字典
    syanten_dict = {seq: result for seq, result in results}

    return syanten_dict


if __name__ == "__main__":
    if os.path.exists("./data/seqs.pkl.gz"):
        print("Loading seqs.pkl.gz")
        seqs_data = pickle.loads(gzip.open("./data/seqs.pkl.gz", "rb").read())
    else:
        seqs_data = generate_seqs_set()
        gzip.open("./data/seqs.pkl.gz", "wb").write(pickle.dumps(seqs_data))

    def save_dict(syanten_dict: dict):
        gzip.open("./data/syanten.pkl.gz", "wb").write(pickle.dumps(syanten_dict))

    b = syanten_dict(seqs_data)
    # 比较 a 和 b 是否相等
    for k, v in a.items():
        if v != b[k]:
            print(k, v, b[k])
