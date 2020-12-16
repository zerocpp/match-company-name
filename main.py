import jieba
import jieba.posseg as pseg
import csv
import jsonlines
import zzpy as z

jieba.enable_paddle()

case_dir = "files2"

splits = list()
with open(f"{case_dir}/names.csv", "r", encoding="utf-8") as fr:
    r = csv.reader(fr)
    for (name,) in z.pb(r):
        result = pseg.lcut(name, use_paddle=True)
        info = {
            "name": name,
            "result": [i.word for i in result]
        }
        splits.append(info)


total_count = 0
words = dict()
for it in splits:
    for key in it.get("result", []):
        words[key] = words.get(key, 0) + 1
        total_count += 1


idf = list()
for word in words:
    count = words[word]
    weight = total_count / count
    idf.append((word, weight))


# name = item["name"]
# words = [i[0] for i in item["result"]]
# item["vector"] = [words.count(i["word"]) * i["weight"] for i in idf]
# fw.write(item)
