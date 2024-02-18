
'''
워크넷 빅데이터 검색 후 채용정보에서 링크 내부로 들어가기
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


cnt = 1
max_page_num=2 # 몇번째 페이지까지 넘길건지
word_list = []
data_dict = {"모집직종":[],
             "직무내용":[],
             "경력조건":[],
             "학력":[],
             "전공":[],
             "자격면허":[],
             "우대조건":[]}

# main문
driver = webdriver.Chrome()

for page_num in range(1, max_page_num+1):
    URL_list = []

    url = f"https://m.work.go.kr/wnSearch/unifSrchResult.do?keyword=%EB%8D%B0%EC%9D%B4%ED%84%B0&srchSort=10&Query=%EB%8D%B0%EC%9D%B4%ED%84%B0&tabName=tb_workinfo&menu=workInfo&pageIndex={page_num}"

    # URL에서 HTML 가져오기
    driver.get(url)


    # BeautifulSoup을 사용하여 HTML 파싱
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # 파싱된 HTML 출력
    # print(soup.prettify())

    # #dataList_2
    for row in soup.select("#dataList_2>li>a"):
        driver.execute_script(row["href"])

        time.sleep(2) # sleep 안넣으면 속도차 때문에 page_source불러올 때 오류남
        html = driver.page_source

        inner_soup = BeautifulSoup(html, 'html.parser')
        # print(inner_soup.prettify()) # html코드보기

        # 모집요강, 우대사항 거르기
        for table in inner_soup.select("table.tb_view01"):
            caption = list(table.stripped_strings)[0] # index 0번이 caption 정보
            # print(caption) # table 이름

            # print(caption)
            if caption in ["모집요강", "우대사항"]:
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

        driver.back()  # 이전 창으로 복구


# print(data_dict)
driver.quit()
df = pd.DataFrame.from_dict(data=data_dict)
print(df)

# df.to_csv('work_net_bigdata.csv', sep=',', na_rep='NaN', encoding='utf-8')