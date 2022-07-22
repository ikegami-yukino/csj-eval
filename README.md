# csj-eval
This repository aims at evaluating speech recognition system using the Corpus of Spontaneous Japanese (CSJ)

CSJ is available at [https://pj.ninjal.ac.jp/corpus_center/csj/](https://clrd.ninjal.ac.jp/csj/index.html)

## Preparation

### Step 1: Install dependencies

```
$ pip install -r requirements.txt
```

```
$ pip install -r chrome/requirements.txt
```

### Step 2: Splits CSJ's wav files per sentence

```
$ ./split_wav.py --ignore_tag --ignore_kansuuji --ignore_anonymization --core /Volumes/Untitled/
```

## Evaluation

### Create recognized results from wav file by speech recognition system

In this repository, `webkitSpeechRecognition` in the Google Chrome is used as a baseline.

At first, run the Web application server as the following:

```
$  ./chrome/server.py
```

Next, open http://127.0.0.1:5000/ by Google Chrome.

Futhermore, connect a USB audio interface to your computer.

Finally, play wav files as the following:

```
$ ./play_wav.py --interval 2.0
```

After executing above commands, `chrome/chrome_result.txt` is created.

### Calculate Word-Error-Rate (WER)

```
$ ./wer.py chrome/chrome_result.txt
```
