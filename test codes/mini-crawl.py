from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request

with urllib.request.urlopen("http://mini.snu.kr/cafe/today/") as url:
    doc = url.read()
    soup = BeautifulSoup(doc, "html.parser")
    table = soup.find("table")
    # print(table)

    # results = {}
    # for row in table.findAll('tr'):
    #     aux = row.findAll('td')
    #     results[aux[0].string] = aux[1].string

    trs = table.findAll('tr')
    flag = ""
    menu = {}
    for tr in trs:
        if tr.text in ["아침", "점심", "저녁"]:
            flag = tr.text
            print(flag)
            print("====")
            continue
        # print(tr.select("td")[0].text)
        # print(str(tr.select("td")[1]).replace("<td class=\"menu\">", "").replace("</td>", ""))
        menu[tr.select("td")[0].text] = str(tr.select("td")[1]).replace("<td class=\"menu\">", "").replace("</td>", "")
    
    
    pprint(menu)

    menu["302동"]

