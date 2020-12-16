import zzpy as z
import jsonlines


idf = list()
for item in z.read_jsonline_with_progressbar("files/idf.jsonl"):
    idf.append(item)


with jsonlines.open("files/vectors.jsonl", "w") as fw:
    for index, item in enumerate(z.read_jsonline_with_progressbar("files/splitted.jsonl")):
        if index >= 100:
            break
        # {"name": "紫金县瓦溪镇康辉药店", "result": [["紫金县", "LOC"], ["瓦溪镇", "LOC"], ["康辉", "nr"], ["药店", "n"]]}
        # {"word": "店", "flag": "n", "count": 231500, "weight": 18.649637149028077}
        name = item["name"]
        words = [i[0] for i in item["result"]]
        item["vector"] = [words.count(i["word"]) * i["weight"] for i in idf]
        fw.write(item)
