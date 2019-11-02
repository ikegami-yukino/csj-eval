#!/usr/bin/env python
import os

from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/chrome/<sentence>')
def write(sentence):
    fdir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(fdir, 'chrome_result.txt'), 'a+') as f:
        f.write(sentence + '\n')


if __name__ == "__main__":
    app.run(port=5000)
