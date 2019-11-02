#!/usr/bin/env python
import argparse
import glob
import os

from pydub import AudioSegment
import tqdm

KANSUUJI = ("一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千")


def parse_timerange(line):
    (start, end) = line.split(" ")[1].split("-")
    start = int(start.replace(".", ""))
    end = int(end.replace(".", ""))
    return (start, end)


def write_wav(basename, csjpath, kind_of_data, start, end, min_wav_size, max_wav_size):
    source_path = os.path.join(csjpath, "WAV", kind_of_data, basename) + ".wav"
    source_sound = AudioSegment.from_file(source_path, format="wav")
    trimmed_sound = source_sound[start:end]
    dest = os.path.join("wav/", "%s_%s-%s.wav" % (basename, start, end))
    trimmed_sound.export(dest, format="wav")
    if min_wav_size < os.path.getsize(dest) < max_wav_size:
        return True
    os.remove(dest)
    return False


def filtering(line, ignore_tag, ignore_anonymization, ignore_kansuuji):
    if ignore_tag and ("(" in line or ")" in line or "<" in line or ">" in line):
        return True
    if ignore_anonymization and "×" in line:
        return True
    if ignore_kansuuji and any(n in line for n in KANSUUJI):
        return True
    return False


def main(csjpath, core, ignore_tag, ignore_anonymization, ignore_kansuuji,
         min_wav_size, max_wav_size):
    kind_of_data = "core" if core else "noncore"
    trn_paths = glob.glob(os.path.join(csjpath, "TRN/Form2", kind_of_data, "*.trn"))
    for source_path in tqdm.tqdm(trn_paths):
        basename = os.path.basename(source_path)[:-4]
        with open(source_path, encoding="cp932") as f:
            for line in f:
                if filtering(line, ignore_tag, ignore_anonymization, ignore_kansuuji):
                    continue
                (start, end) = parse_timerange(line)
                transcription = line.split(" ")[2][2:]
                if transcription:
                    if not write_wav(basename, csjpath, kind_of_data, start, end,
                                     min_wav_size, max_wav_size):
                        continue
                    with open(os.path.join("trn/", "%s_%s-%s.trn" % (basename, start, end)), "w") as f:
                        f.write(transcription + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csjpath", type=str, help="Root path of CSJ's USB memory")
    parser.add_argument("--core", action="store_true",
                        help="Use core data (when this isn't set, use noncore data)")
    parser.add_argument("--ignore_tag", action="store_true",
                        help="Ignore transcription including tag (e.g. <雑音>, (F))")
    parser.add_argument("--ignore_kansuuji", action="store_true",
                        help="Ignore transcription including Chinese numeral (e.g. 一, 十)")
    parser.add_argument("--ignore_anonymization", action="store_true",
                        help="Ignore transcription including ×")
    parser.add_argument("--min_wav_size", type=int, default=60000,
                        help="Threshold of minimum single WAV file size (Bytes)")
    parser.add_argument("--max_wav_size", type=int, default=1000000,
                        help="Threshold of maximum single WAV file size (Bytes)")
    args = parser.parse_args()
    main(args.csjpath, args.core, args.ignore_tag, args.ignore_anonymization, args.ignore_kansuuji,
         args.min_wav_size, args.max_wav_size)
