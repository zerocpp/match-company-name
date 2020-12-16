import zzpy as z
import jsonlines


words = dict()
for it in z.read_jsonline_with_progressbar("splitted.jsonl"):
    for k in it.get("result", []):
        key = tuple(k)
        words[key] = words.get(key, 0) + 1
# print(len(words))
words = [(k[0], k[1], v) for k, v in words.items()]
words = sorted(words, key=lambda i: -i[2])
# print(words[:10])
# print(words[-10:])
with jsonlines.open("words.jsonl", "w") as fw:
    for word, flag, count in words:
        fw.write({
            "word": word,
            "flag": flag,
            "count": count,
        })
