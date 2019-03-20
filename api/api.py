#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'snubob api server'

@app.route('/api/telephone', methods=['POST'])
def telephone():
    phone = {
        "감골식당":"02-880-5544",
        "동원관":"02-880-8697",
        "학생회관":"02-880-5543",
        "아름드리(예술)":"02-876-1006"
    }
    req = request.get_json()
    rest_name = req["action"]["detailParams"]["restaurant_name"]["value"]
    answer = "{}의 전화번호는 <br> {} 입니다.".format(rest_name.encode('utf-8'), phone[rest_name.encode('utf-8')])
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }
    return jsonify(res)

@app.route('/api/menu', methods=['POST'])
def menu():
    

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
