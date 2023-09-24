# %%
import gzip
from core.generator import generate_seqs_set
from core.to_bin import get_seq_int, decode
res = (get_seq_int([[2]]))
print(res)
print(bin(res))
print(hex(res))

print(decode()[res])

flag = False
data = []
# with gzip.open("./data/syanten.gz", "rt") as file:
#     lines = file.readlines()
#     for i in lines:
#         data.append(i)
#         if flag:
#             print(i)
#             break
#         if i.strip() == "20800000000000":
#             print("find")
#             flag = True
# print(data[-1])
# %%
s = generate_seqs_set()

#%%
data = [
  [ 1 ],
  [ 1 ],
  [ 1 ],
  [ 1 ],
  [ 1 ],
  [ 1, 1, 1 ],
  [ 1, 1, 1, 2, 1 ],
  [ 1, 1, 2, 2, 1 ],
]
# to tuple tuple
data = tuple(tuple(i) for i in data)
data
data in s