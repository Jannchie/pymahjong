import multiprocessing
import pickle
import gzip
import os

import tqdm

from core.generator import generate_seqs_set

syanten_dict = None


def syanten(seq_tuple: tuple[tuple[int]], use_table=True) -> int:
    """计算向听数

    Args:
        seq_tuple (tuple[tuple[int]]): 排序手牌序列

    Returns:
        int: 向听数, 0 为听牌, -1 为和牌
    """
    if use_table:
        load_or_generate_table()

    seq = [list(i) for i in seq_tuple]
    nums = 0

    data = {"pos": [[], [], [], [], []]}

    for i in range(len(seq)):
        for j in range(0, len(seq[i]), 2):
            nums += seq[i][j]

    # 如果总牌数不是 3n - 1 或 3n - 2，则将其补齐为 3n - 1，补的牌视作孤张
    while nums % 3 != 2:
        seq.insert(0, (1,))
        nums += 1

    if syanten_dict is not None:
        return syanten_dict[tuple(sorted([tuple(t) for t in seq]))]

    # 预处理
    # 1. 获取可能的 0.雀头、1.顺子、2.刻子、3.搭子、4.对子
    # 2. 获取总牌数
    for i in range(len(seq)):
        for j in range(0, len(seq[i]), 2):
            # nums += seq[i][j]
            if seq[i][j] >= 2:  # 雀头，对子
                data["pos"][0].append((i, j))
                data["pos"][4].append((i, j))
            if seq[i][j] >= 3:  # 刻子
                data["pos"][2].append((i, j))
            if (
                j < len(seq[i]) - 4
                and seq[i][j] >= 1
                and seq[i][j + 2] >= 1
                and seq[i][j + 4] >= 1
                and seq[i][j + 1] == 1
                and seq[i][j + 3] == 1
            ):  # 顺子
                data["pos"][1].append((i, j))
            if j < len(seq[i]) - 2 and seq[i][j] >= 1 and seq[i][j + 2] >= 1:  # 搭子
                data["pos"][3].append((i, j))

    data["k"] = int((nums - 2) / 3)
    data["menzu"] = 0
    data["dazu"] = 0
    data["s_min"] = 8
    for has_atama in atama_iter(seq, data["pos"][0]):  # 迭代所有雀头
        data["atama"] = 1 if has_atama else 0
        pop_menzu(seq, data, nums - 2 if has_atama else nums, has_atama, 0)
    return data["s_min"]


def load_or_generate_table():
    global syanten_dict
    if os.path.exists("./data/syanten.pkl.gz"):
        if syanten_dict is None:
            print("Loading syanten dict")
            syanten_dict = pickle.loads(gzip.open("./data/syanten.pkl.gz", "rb").read())
    else:
        print("Cannot found table, Generating syanten dict")
        syanten_dict = generate_syanten_dict()


def get_nums(seq: list[list[int]]) -> int:
    """获取手牌张数

    Args:
        seq (list[list[int]]): 手牌序列

    Returns:
        int: 手牌张数
    """
    nums = 0
    for i in range(len(seq)):
        for j in range(0, len(seq[i]), 2):
            nums += seq[i][j]
    return nums


def atama_iter(seq: list[list[int]], data: tuple[int, int]) -> list[list[int]]:
    """取出雀头

    Args:
        seq (list[list[int]]): 手牌序列

    Returns:
        list[list[int]]: 取出雀头后的手牌序列
    """
    for i, j in data:
        if seq[i][j] >= 2:
            # 取出雀头
            seq[i][j] -= 2
            yield True
            seq[i][j] += 2
    yield False


def pop_menzu(
    seq: list[list[int]],
    data: list[tuple[int, int]],
    nums: int,
    has_atama: bool,
    menzu=0,
) -> int:
    """
    取面子
    """
    if data["s_min"] == -1:
        return -1
    if nums >= 3:  # 如果还有 3 张牌以上，才可能有完整顺子或刻子
        for i, j in data["pos"][1]:  # 顺子
            if (
                j < len(seq[i]) - 4
                and seq[i][j] >= 1
                and seq[i][j + 2] >= 1
                and seq[i][j + 4] >= 1
                and seq[i][j + 1] == 1
                and seq[i][j + 3] == 1
            ):
                # 有间隔为 1 的三张（顺子）,则取出
                seq[i][j] -= 1
                seq[i][j + 2] -= 1
                seq[i][j + 4] -= 1
                data["menzu"] += 1
                pop_menzu(seq, data, nums - 3, has_atama, menzu + 1)
                data["menzu"] -= 1
                seq[i][j] += 1
                seq[i][j + 2] += 1
                seq[i][j + 4] += 1
        for i, j in data["pos"][2]:  # 刻子
            if seq[i][j] >= 3:
                # 同一种牌有三张，取出刻子
                seq[i][j] -= 3
                data["menzu"] += 1
                pop_menzu(seq, data, nums - 3, has_atama, menzu=menzu + 1)
                data["menzu"] -= 1
                seq[i][j] += 3
    syanten_other(seq, data, nums, has_atama)


def syanten_other(
    seq: list[list[int]],
    data: list[tuple[int, int]],
    nums: int,
    has_atama: bool,
) -> int:
    """
    取搭子
    """

    # 如果当前场况已经不可能小于当前计算出的最小向听数，则提前返回
    if data["dazu"] + (nums - data["atama"] * 2 - data["dazu"]) // 3 >= data["s_min"]:
        return

    # 已经不可能有更小的向听数了（胡牌），直接返回
    if data["s_min"] == -1:
        return

    # 搭子溢出，要拆搭子
    if data["menzu"] + data["dazu"] > data["k"]:
        return

    if nums >= 2:  # 如果还有 2 张牌以上，才可能有搭子
        for i, j in data["pos"][3]:  # 搭子
            if j < len(seq[i]) - 2 and seq[i][j] >= 1 and seq[i][j + 2] >= 1:
                seq[i][j] -= 1
                seq[i][j + 2] -= 1
                data["dazu"] += 1
                syanten_other(seq, data, nums - 2, has_atama)
                data["dazu"] -= 1
                seq[i][j] += 1
                seq[i][j + 2] += 1
        for i, j in data["pos"][4]:  # 对子
            if seq[i][j] >= 2:
                seq[i][j] -= 2
                data["dazu"] += 1
                syanten_other(seq, data, nums - 2, has_atama)
                data["dazu"] -= 1
                seq[i][j] += 2

    data["s_min"] = min(
        2 * (data["k"] - data["menzu"]) - data["dazu"] - data["atama"], data["s_min"]
    )


def calculate_syanten(seq):
    return (seq, syanten(seq))


def save_dict(syanten_dict: dict):
    gzip.open("./data/syanten.pkl.gz", "wb").write(pickle.dumps(syanten_dict))


def generate_syanten_dict():
    seqs_data = generate_seqs_set()
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
    save_dict(syanten_dict)
    return syanten_dict
