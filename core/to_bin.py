# %%
import base64
import os
import pickle
import gzip

path = "./data/syanten.pkl.gz"
if os.path.exists(path):
    syanten_dict = pickle.loads(gzip.open(path, "rb").read())

from tqdm import tqdm


def get_bin_4(num: int) -> int:
    if num == 1:
        return 0b00
    elif num == 2:
        return 0b01
    elif num == 3:
        return 0b10
    elif num == 4:
        return 0b11


def get_bin_3(num: int) -> int:
    if num == 0:
        return 0b00
    elif num == 1:
        return 0b01
    elif num == 2:
        return 0b10


def get_bin_7(num: int) -> int:
    if num == -1:
        return 0b111
    elif num < 7:
        return num
    else:
        raise ValueError("num must be in [-1, 6]")


def int_to_shortest_str(n: int) -> str:
    return base64.b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big")).decode()


def shortest_str_to_int(s: str) -> int:
    return int.from_bytes(base64.b64decode(s), "big")


def int_to_base62(n):
    charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    base = len(charset)
    result = []

    while n > 0:
        n, remainder = divmod(n, base)
        result.append(charset[remainder])

    return "".join(result[::-1] if result else "0")


def get_seq_int(seq):
    n = 0
    res = 0b0
    for sub_seq in seq:
        for idx, el in enumerate(sub_seq):
            if idx % 2 == 0:
                res = res << 2
                res += get_bin_4(el)
                n += 2
            else:
                res = res << 2
                res += get_bin_3(el)
                n += 2
        res = res << 2
        n += 2
        res += 0b00
    res += 0b11
    res <<= 56 - n
    return res


def encode():
    prev = 0
    sorted_key = sorted(syanten_dict.keys())
    data = []
    for seq in tqdm(sorted_key):
        v = syanten_dict[seq]
        res = get_seq_int(seq)
        res <<= 3
        res += get_bin_7(v)
        data.append(res)
        if seq == ((2,),):
            print("find")
            print(res)
            print(bin(res))
            print(v)
            print(res >> 3)

    prev = 0
    with gzip.open("syanten.gz", "wt") as file:
        for res in tqdm(sorted(data)):
            diff: int = res - prev
            prev = res
            file.write(hex(diff)[2:] + "\n")


def decode():
    with gzip.open("./data/syanten.gz", "rt") as file:
        lines = file.readlines()

    prev = 0
    restored_data = {}
    i = 0

    for line in lines:
        diff_hex = line.strip()  # 移除行末尾的换行符
        diff = int(diff_hex, 16)
        original_value = prev + diff
        prev = original_value
        seq, val = original_value >> 3, original_value & 0b111
        restored_data[seq] = -1 if val == 0b111 else val
        i += 1
        # if i % 10000 == 0:
        #     print(seq, original_value)
    return restored_data