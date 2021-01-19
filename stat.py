import csv
import zzpy as z
import pandas as pd


def load_stop_words(file):
    return set(z.read_file(file).split("\n"))


def filter_word_tf(word_tf, idf_threshold=None):
    new_word_tf = dict()
    if idf_threshold:
        for w in word_tf:
            if word_tf[w] >= idf_threshold:
                new_word_tf[w] = word_tf[w]
    return new_word_tf


def stat(input, output, stop_words_file, idf_threshold=None):
    """统计分词结果"""
    df = pd.read_csv(input)
    stop_words = load_stop_words(stop_words_file)
    word_tf = dict()
    for it in df["分词"].values:
        for i in it.split("|"):
            if i in stop_words:
                continue
            word_tf[i] = word_tf.get(i, 0) + 1
    word_tf = filter_word_tf(word_tf=word_tf, idf_threshold=idf_threshold)
    df = pd.DataFrame(
        sorted(word_tf.items(), key=lambda it: -it[1]), columns=["词", "词频"]
    )
    df.to_csv(output, index=0)


def main():
    stat(
        input="output/cut-result.csv",
        output="output/word-stat.csv",
        stop_words_file="file/stop_words.txt",
        idf_threshold=1000,
    )


if __name__ == "__main__":
    main()
