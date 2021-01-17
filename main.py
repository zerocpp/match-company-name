import jieba
import jieba.posseg as pseg
import csv
import jsonlines
import zzpy as z
import math

jieba.enable_paddle()

CASE_DIR = "files1"


def split_name(name):
    # result = jieba.cut(name)
    # return list(result)
    result = pseg.lcut(name, use_paddle=True)
    return list(map(tuple, result))


def calc_idf():
    """
    1. 分词
    """
    print("开始分词")
    with open(f"{CASE_DIR}/input/std.csv", "r", encoding="utf-8") as fr, jsonlines.open(f"{CASE_DIR}/output/std.jsonl", "w") as fw:
        r = csv.reader(fr)
        for (name,) in z.pb(r):
            fw.write({
                "name": name,
                "result": split_name(name),
            })

    """
    2. 统计词频
    """
    words = dict()
    for it in z.read_jsonline_with_progressbar(f"{CASE_DIR}/output/std.jsonl", title="统计词频"):
        # for key in it.get("result", []):
        for k in it.get("result", []):
            key = k[0]
            words[key] = words.get(key, 0) + 1
    words = [(k, v) for k, v in words.items()]
    words = sorted(words, key=lambda i: -i[1])
    with jsonlines.open(f"{CASE_DIR}/output/word_count.jsonl", "w") as fw:
        for word, count in words:
            fw.write({
                "word": word,
                "count": count,
            })

    """
    3. 计算IDF
    """
    total_count = 0
    for item in z.read_jsonline_with_progressbar(f"{CASE_DIR}/output/word_count.jsonl", title="统计词频总数"):
        total_count += item["count"]

    with jsonlines.open(f"{CASE_DIR}/output/idf.jsonl", "w") as fw:
        for item in z.read_jsonline_with_progressbar(f"{CASE_DIR}/output/word_count.jsonl", title="计算IDF"):
            item["weight"] = total_count / item["count"]
            fw.write(item)


def load_idf():
    """
    加载IDF
    """
    idf = dict()
    for item in z.read_jsonline_with_progressbar(f"{CASE_DIR}/output/idf.jsonl", title="加载IDF"):
        idf[item["word"]] = item["weight"]
    return idf


def gen_vector(name, slices=[], idf=[]):
    if not slices:
        slices = split_name(name)
        print(f"{name}: {slices}")
        slices = [s[0] for s in slices]
    if not idf:
        idf = list(z.read_jsonline(f"{CASE_DIR}/output/idf.jsonl"))
    vector = []
    for item in idf:
        word, weight = item["word"], item["weight"]
        if word in slices:
            vector.append(weight)
        else:
            vector.append(0)
    return vector


def gen_vectors():
    """
    生成向量
    """
    idf = list(z.read_jsonline(f"{CASE_DIR}/output/idf.jsonl"))

    with jsonlines.open(f"{CASE_DIR}/output/vectors.jsonl", "w") as fw:
        for it in z.read_jsonline_with_progressbar(f"{CASE_DIR}/output/std.jsonl", title="生成向量"):
            name = it.get("name", "")
            # keys = [key for key in it.get("result", [])]
            keys = [key for key, _ in it.get("result", [])]
            vector = gen_vector(name=name, slices=keys, idf=idf)
            fw.write({
                "name": name,
                "vector": vector,
            })


def cosine_distance(a, b):
    # todo
    """
    /Users/zero/code/match-company-name/main.py:104: RuntimeWarning: invalid value encountered in double_scalars
  similiarity = np.dot(a, b.T) / (a_norm * b_norm)
  """
    import numpy as np
    a = np.array(a)
    b = np.array(b)
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if not a_norm or not b_norm:
        return np.inf
    similiarity = np.dot(a, b.T) / (a_norm * b_norm)
    return 1. - similiarity


def calc_vec(vector):
    vectors = z.read_jsonline(f"{CASE_DIR}/output/vectors.jsonl")
    scores = []
    for v in z.pb(vectors, title="计算分数"):
        name = v["name"]
        if not name:
            continue
        vec = v["vector"]
        dist = cosine_distance(vector, vec)
        # score = round((1.0-dist)*100.0, 6)
        score = round(dist, 6)
        scores.append((name, score))
    scores = sorted(scores, key=lambda it: it[1])
    return scores


def calc_score(name, idf):
    vec = gen_vector(name, idf=idf)
    scores = calc_vec(vec)
    return scores[:3]


def main():
    import numpy as np
    np.set_printoptions(precision=6)

    # calc_idf()
    # idf = load_idf()
    # gen_vectors()

    # 计算vector
    idf = list(z.read_jsonline(f"{CASE_DIR}/output/idf.jsonl"))
    names = [
        "紫金县瓦溪镇康辉药店", "瓦溪镇康辉药店", "紫金瓦溪镇康辉药店", "紫金县瓦溪镇康辉药房",
        "武汉市江岸区李永康西医内科诊所", "武汉市江岸区李永康诊所", "江岸区李永康诊所",
    ]
    with jsonlines.open(f"{CASE_DIR}/output/scores.jsonl", "w") as fw:
        for name in names:
            scores = calc_score(name, idf)
            fw.write({
                "name": name,
                "scores": scores,
            })
            print(name, scores)
    print("exit")


if __name__ == "__main__":
    main()
