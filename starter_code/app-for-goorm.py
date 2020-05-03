import os
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
	return "snubob api server"

@app.route("/hello")
def hello():
    return "hellp, snubob"


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(sys.argv[1]))