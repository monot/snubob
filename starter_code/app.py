import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# home route - check server status
@app.route('/')
def hello():
    return 'snubob api server'

# your codes will be here.

if __name__=="__main__":
    # app.run() # for production
    # app.run(debug=True) # for debugging purpose
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080))) # for cloud9
