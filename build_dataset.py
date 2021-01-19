import zzpy as z
import json
import pandas as pd


def load_cut_result(cut_result_csv):
    df = pd.read_csv(cut_result_csv)
    cut_result = dict()
    for name, it in df.values:
        words = set(it.split("|"))
        cut_result[name] = words
    return cut_result


def build_dataset(cut_result, words):
    """以所有分词为特征，行业库分类结果为标签，建立数据集"""

    head = ["行业库名称", "行业库分类"] + words
    result = [head]

    for it in z.read_jsonline_with_progressbar(
        "/Users/zero/Downloads/行业库数据/lgd.jsonl", title="构建分类数据集"
    ):
        name = it["name"]
        type_names = it["type_names"]
        # s[type_names] = s.get(type_names, 0) + 1
        row = [name, type_names] + [
            1 if w in cut_result.get(name, set()) else 0 for w in words
        ]
        result.append(row)
    return result


if __name__ == "__main__":
    cut_result_csv = "output/cut-result.csv"
    stop_words_file = "file/stop_words.txt"
    stat_csv = "output/word-stat.csv"
    print("加载所有纬度(词)")
    words = list(pd.read_csv(stat_csv)["词"])
    print("加载分词结果")
    cut_result = load_cut_result(cut_result_csv)
    print("构建分类数据集")
    result = build_dataset(cut_result, words)
    print("保存结果")
    pd.DataFrame(result).to_csv("output/type-dataset.csv", index=0)
