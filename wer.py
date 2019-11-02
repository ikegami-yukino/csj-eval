#!/usr/bin/env python
import argparse
import glob

from jiwer import wer
import MeCab
import numpy as np


def main(target_file_path, mecab_dic):
    paths = sorted(glob.glob("trn/*.trn"))
    mecab_arg = " -d " + mecab_dic if mecab_dic else ""
    t = MeCab.Tagger("-Owakati" + mecab_arg)
    errors = []
    with open(target_file_path) as f:
        for (i, line) in enumerate(f):
            print(paths[i])
            line = line.rstrip()
            hypothesis = t.parse(line).rstrip().split(" ")
            with open(paths[i]) as gtf:
                ground_truth = gtf.read().rstrip()
            ground_truth = t.parse(ground_truth).rstrip().split(" ")
            error = wer(ground_truth, hypothesis)
            print("Ground truth:", " ".join(ground_truth))
            print("Hypothesis:", " ".join(hypothesis))
            print("WER:", error)
            errors.append(error)
    print("Average WER:", np.mean(errors))
    print("Median WER:", np.median(errors))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_file_path", type=str)
    parser.add_argument("--mecab_dic", type=str, help="Path of MeCab dictionary")
    args = parser.parse_args()

    main(args.target_file_path, args.mecab_dic)
