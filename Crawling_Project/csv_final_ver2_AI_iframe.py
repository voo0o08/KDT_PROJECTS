
'''
워크넷 AI 검색 후 채용정보에서 링크 내부로 들어가기
'''

import os
import sys
import urllib.request
import json
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import re
from selenium.webdriver.common.by import By # find_element 때문에

def without_iframe(html):
    global cnt, data_dict
    inner_soup = BeautifulSoup(html, 'html.parser')
    # 모집요강, 우대사항 거르기
    for table in inner_soup.select("h3"):
        print()
        caption = list(table.stripped_strings)[0] # index 0번이 caption 정보

        print("이것은 윤서의 캡션 : ",caption) # table 이름
        #print(list(table.next_sibling.next_sibling.stripped_strings))
        # print(caption)
        if caption in ["모집요강", "우대사항"]:
            for element in table.next_sibling.next_sibling.select("table"):
                print(list(element.select_one("thead").stripped_strings))
                print(list(element.select_one("tbody").stripped_strings))


                info_list = table.select("tbody>tr") # 기업정보 row_data
                for info in info_list:
                    detail_list = list(info.stripped_strings)
                    # print(list(info.stripped_strings))
                    # ['모집직종', '데이터 분석가(빅데이터 분석가)', '직업정보']
                    # ['관련직종', '경영 기획 사무원, 총무 및 일반 사무원']
                    if detail_list[0] in data_dict.keys():
                        data_dict[detail_list[0]].append(" ".join(detail_list[1:]))
        else:
            # 무관한 table은 그냥 다음 테이블로 넘어가기
            continue

    # 테이블 다 봤으면 길이 맞춰주기
    for key, val in data_dict.items():
        if len(val) != cnt:
            val.append("-")
    #print()
    cnt += 1



cnt = 1
max_page_num=10 # 몇번째 페이지까지 넘길건지
word_list = []
data_dict = {"우대":[],
             "요건":[],
             "업무":[]}

# main문
driver = webdriver.Chrome()
i =0
for page_num in range(1, max_page_num+1):
    URL_list = []

    url = f"https://work.go.kr/wnSearch/unifSrch.do?regDateStdt=&regDateEndt=&colName=tb_workinfo&srchDateSelected=all&sortField=RANK&sortOrderBy=DESC&searchDateInfo=&temp=&pageIndex={page_num}&tabName=tb_workinfo&dtlSearch=&query=%EB%8D%B0%EC%9D%B4%ED%84%B0&radio_period=on&srchStdt=&srchEndt=&reQuery=&agreeQuery=&prikeyQuery=&exceptQuery="

    # URL에서 HTML 가져오기
    driver.get(url)


    # BeautifulSoup을 사용하여 HTML 파싱
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # 파싱된 HTML 출력
    # print(soup.prettify())
    #print(soup.select(".link"))

    # #dataList_2
    for row in soup.select(".link"):
        print()
        #print("="*50, row.select_one("a")["href"])
        driver.get("https://work.go.kr"+str(row.select_one("a")["href"]))

        time.sleep(0.2) # sleep 안넣으면 속도차 때문에 page_source불러올 때 오류남
        html = driver.page_source
########################### iframe // find_element(By.TAG_NAME,	‘h1’)
        iframe_element = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe_element)

        # iframe 안에서의 동작 수행
        # 예를 들어, iframe 안에서 특정 요소를 찾아서 출력하는 등의 동작을 수행할 수 있습니다.

        # iframe의 HTML 코드 가져오기
        iframe_html = driver.page_source
############################
        inner_soup = BeautifulSoup(iframe_html, 'html.parser')
        # print(inner_soup.prettify()) # html코드보기

        try:
            if inner_soup.select_one("title").text == "채용담당자와 한마디":
                # without_iframe(html)
                pass
            else:
                # 3번
                for tit in inner_soup.select("tbody"):
                    # print(tit.select_one("strong").text)
                    try:
                        if tit.select_one("strong").text in ["주요업무", "우대사항"]:
                            print(tit.text)

                    except:
                        pass

                # 4번
                for tit in inner_soup.select("h2"):
                    # print(i)
                    try:
                         # print(tit.next_sibling.text)
                        text = tit.next_sibling.text
                        for key in data_dict.keys():
                            if key in text:
                                data_dict[key].append(text)
                            else:
                                data_dict[key].append("-")
                    except:
                        pass

        except:
            pass






        driver.back()  # 이전 창으로 복구



print(data_dict)
driver.quit()
df = pd.DataFrame.from_dict(data=data_dict)
print(df)

df.to_csv('iframe_data.csv', sep=',', na_rep='NaN', encoding='utf-8')