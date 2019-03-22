#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request
import pyjosa

app = Flask(__name__)

# 0:today, 1:tomorrow
def get_menu(day=0):
    breakfast = {}
    lunch = {}
    dinner = {}
    
    if day == 0:
        menurl = "http://mini.snu.kr/cafe/today"
    elif day == 1:
        menurl = "http://mini.snu.kr/cafe/tomorrow"
        
    with urllib.request.urlopen(menurl) as url:
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
            rest_val = str(tr.select("td")[1]).replace("<td class=\"menu\">", "").replace("</td>", "").replace("</span>", " ").replace('<span class="price">', "").replace('<span class="supple">', " ").replace("<br/>", "\n").replace("&amp;", " & ").replace("\n\n", "\n")

            if flag == "아침":
                breakfast[rest_key] = rest_val
            if flag == "점심":
                lunch[rest_key] = rest_val
            if flag == "저녁":
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
        "아름드리(예술)":"02-876-1006",
        "소담마루":"02-880-8698",
        "교수회관":"02-880-5241",
        "다향만당":"02-880-6244",
        "퀴즈노즈":"02-871-9329",
        "호암교수회관":"02-880-6797",
        "라쿠치나":"02-880-1631",
        "자하연":"02-880-7889",
        "샤반":"02-871-6933",
        "락구정":"02-875-8840"
    }
    req = request.get_json()
    rest_name = req["action"]["detailParams"]["restaurant_name"]["value"]
    answer = "{}의 전화번호는\n{} 입니다.".format(rest_name, phone[rest_name])
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

# 메뉴를 불러옴.
# 패러미터로 restaurant_name, ***를 사용
@app.route('/api/menu', methods=['POST'])
def menu():
    req = request.get_json()
    try:
        rest_name = req["action"]["detailParams"]["restaurant_name"]["value"]
    except KeyError:
        rest_name = 0
    
    try:
        sys_date = req["action"]["detailParams"]["sys.date"]["value"]
    except KeyError:
        sys_date = 0
    
    try:
        sys_timep = req["action"]["detailParams"]["sys.time.period"]["value"]
    except KeyError:
        sys_timep = 0
    
    breakfast, lunch, dinner = get_menu()
    breakfast_menu = breakfast.get(rest_name, 0)
    lunch_menu = lunch.get(rest_name, 0)
    dinner_menu = dinner.get(rest_name, 0)

    menu = ""
    if breakfast_menu != 0:
        menu += "\n\n== 아침 ==\n{}".format(breakfast_menu)
    if lunch_menu != 0:
        menu += "\n\n== 점심 ==\n{}".format(lunch_menu)
    if dinner_menu != 0:
        menu += "\n\n== 저녁 ==\n{}".format(dinner_menu)

    if menu == "":
        answer = pyjosa.replace_josa("{}(은)는 {} 쉽니다.".format(rest_name, date_string))
    else:
        answer = "{}의 {} 메뉴는 다음과 같습니다.{}".format(rest_name, date_string, menu)

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

    
if __name__=="__main__":
    # app.run() # production
    app.run(debug=True) # for debugging purpose
    # app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))