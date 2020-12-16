import zzpy as z
import jsonlines


total_count = 0
for item in z.read_jsonline_with_progressbar("files/words.jsonl"):
    total_count += item["count"]

with jsonlines.open("files/idf.jsonl", "w") as fw:
    for item in z.read_jsonline_with_progressbar("files/words.jsonl"):
        item["weight"] = total_count / item["count"]
        fw.write(item)
