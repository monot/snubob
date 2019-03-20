#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request

app = Flask(__name__)

def get_menu():
    breakfast = {}
    lunch = {}
    dinner = {}
    with urllib.request.urlopen("http://mini.snu.kr/cafe/today/") as url:
        doc = url.read()
        soup = BeautifulSoup(doc, "html.parser")
        table = soup.find("table")

        trs = table.findAll('tr')
        flag = ""
        
        for tr in trs:
            if tr.text in ["아침", "점심", "저녁"]:
                flag = tr.text
                # print(flag)
                continue
            rest_key = tr.select("td")[0].text
            rest_val = str(tr.select("td")[1]).replace("<td class=\"menu\">", "").replace("</td>", "").replace("</span>", "</span> ")

            if flag.encode('utf-8') == "아침":
                breakfast[rest_key] = rest_val
            if flag.encode('utf-8') == "점심":
                lunch[rest_key] = rest_val
            if flag.encode('utf-8') == "저녁":
                dinner[rest_key] = rest_val
    return (breakfast, lunch, dinner)

##

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
    answer = "{}의 전화번호는<br>{} 입니다.".format(rest_name.encode('utf-8'), phone[rest_name.encode('utf-8')])
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
    req = request.get_json()
    rest_name = req["action"]["detailParams"]["restaurant_name"]["value"]
    sys_date = req["action"]["detailParams"]["sys_date"]["value"]
    
    breakfast, lunch, dinner = get_menu()
    answer = "{}의 오늘 메뉴는 다음과 같습니다.<br><br>{}{}{}".format(rest_name.encode('utf-8'), breakfast[rest_name.encode('utf-8')], lunch[rest_name.encode('utf-8')], dinner[rest_name.encode('utf-8')])
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

    

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
