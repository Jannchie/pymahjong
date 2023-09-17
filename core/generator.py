from tqdm import tqdm


def seq_generator(n: int, max_val=4, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    ans = []
    if n == 0:
        return [[]]

    for i in [1, 2, 3, 4]:
        if n >= i:
            for x in seq_generator(n - i, max_val, memo):
                ans.append([i] + x)
    memo[n] = ans
    return ans


def div_generator(n=13, amount=0, memo=None):
    if memo is None:
        memo = {}
    if n < 1:
        return [[]]
    if (n, amount) in memo:
        return memo[(n, amount)]
    ans = []
    for i in [0, 1, 2]:
        if i == 0:
            for x in div_generator(n - 1, 0, memo):
                ans.append([0] + x)
        elif amount + i <= 8:
            for x in div_generator(n - 1, amount + i, memo):
                ans.append([i] + x)
    memo[(n, amount)] = ans
    return ans


def generate_seqs_set() -> set[tuple[tuple[int]]]:
    dividers = {n: div_generator(n) for n in range(1, 14)}
    seqs = [x for n in [2, 5, 8, 11, 14] for x in seq_generator(n)]
    ans = set()
    for seq in tqdm(seqs, desc="Generating sorted sequences", unit="seq"):
        if len(seq) == 1:
            ans.add(tuple([tuple(seq)]))
            continue
        d = dividers[len(seq) - 1]
        for x in d:
            res = []
            i = 0
            cur = [seq[i]]  # cur = [1]
            while i < len(x):
                if x[i] == 0:
                    res.append(tuple(cur) if cur < cur[::-1] else tuple(cur[::-1]))
                    cur = [seq[i + 1]]
                else:
                    cur += [x[i], seq[i + 1]]
                i += 1
            if cur:
                res.append(tuple(cur) if cur < cur[::-1] else tuple(cur[::-1]))
            ans.add(tuple(sorted(res)))
    return ans
