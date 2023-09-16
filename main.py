# %%
import multiprocessing
import os
from core.generator import generate_sorted_seqs_set
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
    syanten_data = pickle.loads(gzip.open("./data/syanten.pkl.gz", "rb").read())
    pass
    for key in syanten_data.keys():
        if len(key) == 1 and len(key[0]) == 1:
            print(key)
    # if os.path.exists("./data/seqs.pkl.gz"):
    #     print("Loading seqs.pkl.gz")
    #     seqs_data = pickle.loads(gzip.open("./data/seqs.pkl.gz", "rb").read())
    # else:
    #     seqs_data = generate_sorted_seqs_set()
    #     gzip.open("./data/seqs.pkl.gz", "wb").write(pickle.dumps(seqs_data))

    # def save_dict(syanten_dict: dict):
    #     gzip.open("./data/syanten.pkl.gz", "wb").write(pickle.dumps(syanten_dict))

    # save_dict(syanten_dict(seqs_data))
