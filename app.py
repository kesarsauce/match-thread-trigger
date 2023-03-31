import logging
import time

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
    start_time = time.time()
    resp = trigger_match_thread()
    time_taken = time.time() - start_time
    app.logger.info(f"Time taken: {time_taken}s")
    return jsonify(resp)

if __name__ == "__main__":
    app.run()
    
