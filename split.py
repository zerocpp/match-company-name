import jieba
import jieba.posseg as pseg
import csv
import jsonlines
import zzpy as z

jieba.enable_paddle()

case_dir = "files2"

with open(f"{case_dir}/names.csv", "r", encoding="utf-8") as fr, jsonlines.open(f"{case_dir}/split.jsonl", "w") as fw:
    r = csv.reader(fr)
    for (name,) in z.pb(r):
        result = pseg.lcut(name, use_paddle=True)
        info = {
            "name": name,
            "result": list(map(tuple, result))
        }
        fw.write(info)
