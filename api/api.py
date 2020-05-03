#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
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
    # (POST된) JSON 파일 저장
    req = request.get_json()
    # 필요한 키 추출. 키가 없으면 0 리턴 (try..except 대신 get 함수 사용)
    rest_name = req.get("action",{}).get("detailParams",{}).get("restaurant_name",{}).get("value", 0)
    sys_date = req.get("action",{}).get("detailParams",{}).get("sys_date",{}).get("origin", 0)
    sys_timep = req.get("action",{}).get("detailParams",{}).get("meal_time",{}).get("value", 0)
    
    date_string = "오늘"
    time_string = ""
    notice = ""
    breakfast = {}
    lunch = {}
    dinner = {}

    # 만약 오늘/내일 등이 날짜가 지정되면
    if sys_date != 0:     
        if sys_date == "오늘":
            date_string = "오늘"
            breakfast, lunch, dinner = get_menu()
            notice = ""
        elif sys_date == "내일":
            date_string = "내일"
            breakfast, lunch, dinner = get_menu(1)
            notice = ""
        else:
            date_string = "오늘"
            breakfast, lunch, dinner = get_menu()
            notice = "오늘과 내일의 메뉴만 제공합니다.\n"

    # 날짜가 지정되지 않으면
    else:
        date_string = "오늘"
        breakfast, lunch, dinner = get_menu()
    
    breakfast_menu = breakfast.get(rest_name, 0)
    lunch_menu = lunch.get(rest_name, 0)
    dinner_menu = dinner.get(rest_name, 0)

    menu = ""
    # sys_timep가 0이 아닌 경우, 즉, 아침, 점심, 저녁 등의 키워드가 제공된 경우 
    # 해당 시간대의 메뉴를 제공
    if sys_timep != 0:
        if sys_timep in ["아침", "오전", "모닝", "조식"]:
            time_string = "아침"
            if breakfast_menu != 0:
                menu += "\n\n== 아침 ==\n{}".format(breakfast_menu)
        if sys_timep in ["점심", "오후", "중식"]:
            time_string = "점심"
            if lunch_menu != 0:
                menu += "\n\n== 점심 ==\n{}".format(lunch_menu)
        if sys_timep in ["저녁", "밤", "석식"]:
            time_string = "저녁"
            if dinner_menu != 0:
                menu += "\n\n== 저녁 ==\n{}".format(dinner_menu)
        
        if menu == "":
            answer = pyjosa.replace_josa("{}(은)는 {} {}시간에 쉽니다.".format(rest_name, date_string, time_string))
            answer = notice + answer
        else:
            answer = "{} {}의 {}메뉴는 다음과 같습니다.{}".format(date_string, rest_name, time_string, menu)
            answer = notice + answer

    # sys_timep가 0인 경우, 즉 아침, 점심, 저녁이 제공되지 않으면 
    # 하루 전체 메뉴를 제공.
    else:
        if breakfast_menu != 0:
            menu += "\n\n== 아침 ==\n{}".format(breakfast_menu)
        if lunch_menu != 0:
            menu += "\n\n== 점심 ==\n{}".format(lunch_menu)
        if dinner_menu != 0:
            menu += "\n\n== 저녁 ==\n{}".format(dinner_menu)

        if menu == "":
            answer = pyjosa.replace_josa("{} {}(은)는 쉽니다.".format(date_string, rest_name))
            answer = notice + answer
        else:
            answer = "{}의 {} 메뉴는 다음과 같습니다.{}".format(rest_name, date_string, menu)
            answer = notice + answer

    # 답변을 위한 JSON 
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

    # app.run(host='0.0.0.0', port=int(sys.argv[1])) # use this for goorm ide (remove others)