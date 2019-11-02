#!/usr/bin/env python
import argparse
import glob
import os
import platform
import subprocess
import time


def det_play_command():
    if platform.system() == "Windows":
        (_, error) = execute(("where", "sox"))
        if not error:
            return "sox"
        else:
            RuntimeError("sox is not installed. see the following article:"
                         "https://qiita.com/teteyateiya/items/e4dc27e384d947b9946d")
    elif platform.system() == "Darwin":
        return "afplay"
    else:
        for command in ("aplay", "play"):
            (_, error) = execute(("which", command))
            if not error:
                return command
        RuntimeError("Try: sudo apt install alsa-utils")


def execute(cmd):
    proc = subprocess.Popen(cmd, shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (stdout, error) = proc.communicate()
    return (stdout, error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Interval of time (sec.) among utterances")
    args = parser.parse_args()

    play_command = det_play_command()

    paths = glob.glob("wav/*.wav")
    total = len(paths)
    for (count, path) in enumerate(sorted(paths), start=1):
        transcript_path = os.path.join("trn", os.path.basename(path)[:-4] + ".trn")
        with open(transcript_path) as f:
            transcript = f.read().rstrip()
        print("[%s/%s]" % (count, total), transcript)
        command = (play_command, path, "-d") if play_command == "sox" else (play_command, path)
        execute(command)
        time.sleep(args.interval)
