from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request

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

        if flag == "아침":
            breakfast[rest_key] = rest_val
        if flag == "점심":
            lunch[rest_key] = rest_val
        if flag == "저녁":
            dinner[rest_key] = rest_val

pprint(dinner)