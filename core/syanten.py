def syanten(seq_tuple: tuple[tuple[int]]) -> int:
    """计算向听数

    Args:
        seq_tuple (tuple[tuple[int]]): 排序手牌序列

    Returns:
        int: 向听数, 0 为听牌, -1 为和牌
    """
    min_syanten = 8
    seq = [list(i) for i in seq_tuple]
    nums = get_nums(seq)
    for has_atama in atama_iter(seq):  # 迭代所有雀头
        s = pop_menzu(seq, nums - 2 if has_atama else nums, has_atama)
        min_syanten = min(min_syanten, s)
    return min_syanten - 1


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


def atama_iter(seq: list[list[int]]) -> list[list[int]]:
    """取出雀头

    Args:
        seq (list[list[int]]): 手牌序列

    Returns:
        list[list[int]]: 取出雀头后的手牌序列
    """
    for i in range(len(seq)):
        for j in range(0, len(seq[i]), 2):
            if seq[i][j] >= 2:
                # 取出雀头
                seq[i][j] -= 2
                yield True
                seq[i][j] += 2
    yield False


def pop_menzu(seq: list[list[int]], nums: int, has_atama: bool) -> int:
    """
    取面子
    """
    min_syanten = 8
    if nums >= 3:  # 如果还有 3 张牌以上，才可能有完整顺子或刻子
        for i in range(len(seq)):
            for j in range(0, len(seq[i]) - 4, 2):
                if (
                    seq[i][j] >= 1
                    and seq[i][j + 2] >= 1
                    and seq[i][j + 4] >= 1
                    and seq[i][j + 1] == 1
                    and seq[i][j + 3] == 1
                ):
                    # 有间隔为 1 的三张（顺子）,则取出
                    seq[i][j] -= 1
                    seq[i][j + 2] -= 1
                    seq[i][j + 4] -= 1
                    s = pop_menzu(seq, nums - 3, has_atama)
                    min_syanten = min(min_syanten, s)
                    seq[i][j] += 1
                    seq[i][j + 2] += 1
                    seq[i][j + 4] += 1
            for j in range(0, len(seq[i]), 2):
                if seq[i][j] >= 3:
                    # 同一种牌有三张，取出刻子
                    seq[i][j] -= 3
                    s = pop_menzu(seq, nums - 3, has_atama)
                    min_syanten = min(min_syanten, s)
                    seq[i][j] += 3

    res = syanten_other(seq, nums, has_atama)
    return min(min_syanten, res)


def syanten_other(
    seq: list[list[int]], nums: int, has_atama: bool, add: int = 0
) -> int:
    """
    取搭子
    """
    min_syanten = 8
    syanten = 0
    if nums >= 2:  # 如果还有 2 张牌以上，才可能有搭子
        for i in range(len(seq)):
            for j in range(0, len(seq[i]), 2):
                if (
                    j < len(seq[i]) - 2
                    and seq[i][j] >= 1
                    and seq[i][j + 1] == 1
                    and seq[i][j + 2] >= 1
                ):  # 有间隔为 1 的两张（搭子）
                    seq[i][j] -= 1
                    seq[i][j + 2] -= 1
                    syanten = syanten_other(seq, nums - 2, has_atama, add + 1)
                    min_syanten = min(min_syanten, syanten)
                    seq[i][j] += 1
                    seq[i][j + 2] += 1
                if seq[i][j] >= 2:  # 有两张相同的牌（对子）
                    seq[i][j] -= 2
                    syanten = syanten_other(seq, nums - 2, has_atama, add + 1)
                    min_syanten = min(min_syanten, syanten)
                    seq[i][j] += 2
                if (
                    j < len(seq[i]) - 2
                    and seq[i][j] >= 2
                    and seq[i][j + 1] == 2
                    and seq[i][j + 2] >= 1
                ):
                    # 有间隔为 2 的两张（坎张）
                    seq[i][j] -= 1
                    seq[i][j + 2] -= 1
                    syanten = syanten_other(seq, nums - 2, has_atama, add + 1)
                    min_syanten = min(min_syanten, syanten)
                    seq[i][j] += 1
                    seq[i][j + 2] += 1

    # 处理孤张
    # 孤张优先用来补搭子
    nums -= add

    if nums % 3 == 2:
        # 搞到最后还有两张孤张，如果没有雀头则是一向，否则是两向
        if has_atama:
            syanten += 2
        else:
            syanten += 1
        nums -= 2

    if nums % 3 == 1:
        # 搞到最后多了一张孤张，则肯定没有雀头
        syanten += 1
        nums -= 1

    syanten += nums // 3 * 2
    return min(syanten + add, min_syanten)
