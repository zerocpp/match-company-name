import zzpy as z
import json
import pandas as pd


def load_cut_result():
    df = pd.read_csv("output/cut-result.csv")
    stop_words = set(z.read_file("file/stop_words.txt").split("\n"))
    cut_result = dict()
    for name, it in df.values:
        words = set(i for i in it.split("|") if i not in stop_words)
        cut_result[name] = words
    return cut_result


def build_dataset():
    """以所有分词为特征，行业库分类结果为标签，建立数据集"""
    # print("加载分词结果")
    # cut_result = load_cut_result()

    words = list(pd.read_csv("output/word-stat.csv")["词"])
    head = ["行业库名称", "行业库分类"] + words
    result = [head]

    print("构建分类数据集")
    s = dict()
    for it in z.read_jsonline_with_progressbar(
        "/Users/zero/Downloads/行业库数据/lgd.jsonl", title="构建分类数据集"
    ):
        name = it["name"]
        type_names = it["type_names"]
        s[type_names] = s.get(type_names, 0) + 1
        # row = [name, type_names] + [
        #     1 if w in cut_result.get(name, set()) else 0 for w in words
        # ]
        # result.append(row)
    # pd.DataFrame(result).to_csv("output/type-dataset.csv", index=0)
    print(s)


if __name__ == "__main__":
    build_dataset()
