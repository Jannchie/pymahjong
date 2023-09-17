M = [000 + (i + 1) * 10 + j for i in range(9) for j in range(4)]
P = [100 + (i + 1) * 10 + j for i in range(9) for j in range(4)]
S = [200 + (i + 1) * 10 + j for i in range(9) for j in range(4)]
Z = [300 + i * 100 + j for i in range(7) for j in range(4)]
ALL = M + P + S + Z

ALL_DIFFERENT = []
for i in range(3):
    ALL_DIFFERENT += [i * 100 + j * 10 for j in range(1, 10)]
for i in range(3, 10):
    ALL_DIFFERENT += [i * 100]


def get_suit(x: int):
    return x // 100


def get_val(x: int):
    return (100 + x) // 10 % 10


def get_ver(x: int):
    return x % 10


def get_suit_str(x: int):
    if get_suit(x) == 0:
        return "萬"
    elif get_suit(x) == 1:
        return "筒"
    elif get_suit(x) == 2:
        return "條"
    elif 3 <= get_suit(x) <= 9:
        return ["東", "南", "西", "北", "白", "發", "中"][get_suit(x) - 3]
    raise ValueError("Invalid Tile")


def get_val_str(x: int):
    if get_suit(x) >= 3:
        return ["東", "南", "西", "北", "白", "發", "中"][get_suit(x) - 3]
    return ["一", "二", "三", "四", "五", "六", "七", "八", "九"][get_val(x) - 1]


def is_valid(x: int):
    if get_ver(x) >= 5:
        return False
    v = get_val(x)
    if get_suit(x) < 3:
        return 1 <= v <= 9
    else:
        return v == 0


def get_str(x: int):
    if not is_valid(x):
        raise ValueError("Invalid Tile:", x)
    if get_suit(x) >= 3:
        return ["東", "南", "西", "北", "白", "發", "中"][get_suit(x) - 3]
    elif get_ver(x) == 3 and get_val(x) == 5:
        return "赤" + get_val_str(x) + get_suit_str(x)
    else:
        return get_val_str(x) + get_suit_str(x)


def is_same_suit(a: int, b: int):
    return a // 100 == b // 100


def is_same_val(a: int, b: int):
    return get_val(a) == get_val(b)


def is_same(a: int, b: int):
    return is_same_suit(a, b) and is_same_val(a, b)


def is_aka(a: int):
    return get_val(a) == 3 and get_suit(a) < 3
