import logging

from flask import Flask, jsonify
import praw

from scraper import trigger_match_thread


app = Flask(__name__)
app.logger.setLevel(logging.INFO)

import os
@app.route("/ping")
def health_check():
    return "pong"

@app.route("/next-trigger")
def next_trigger():
    resp = trigger_match_thread()
    return jsonify(resp)

if __name__ == "__main__":
    app.run()
    