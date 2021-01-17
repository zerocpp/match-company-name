import jieba
import csv
import zzpy as z

jieba.enable_parallel(4)  # 开启并行分词模式，参数为并行进程数


def cut(input, output):
    """分词"""
    with open(output, mode="w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["名称", "分词"])
        for it in z.read_jsonline_with_progressbar(input, title="分词"):
            name = it["name"]
            result = jieba.lcut(name)
            writer.writerow([name, "|".join(result)])


def main():
    cut(
        input="/Users/zero/Downloads/行业库数据/lgd.jsonl", output="output/cut-result.csv",
    )

