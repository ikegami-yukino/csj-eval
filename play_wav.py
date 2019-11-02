#!/usr/bin/env python
import argparse
import glob
import os
import subprocess
import time


def execute(cmd):
    proc = subprocess.Popen(cmd, shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (stdout, error) = proc.communicate()
    return (stdout, error)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Interval of time (sec.) among utterances")
    args = parser.parse_args()

    paths = glob.glob('wav/*.wav')
    total = len(paths)
    for (count, path) in enumerate(sorted(paths)):
        transcript_path = os.path.join('trn', os.path.basename(path)[:-4] + '.trn')
        with open(transcript_path) as f:
            transcript = f.read().rstrip()
        print('[%s/%s]' % (count, total), transcript)
        execute(('afplay', path))
        time.sleep(args.interval)
