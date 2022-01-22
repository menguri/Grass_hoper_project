# to do list
# 1. 표 안에 있는 데이터 모집
# 2. 조회 버튼 에러 해결
# 3. 수집한 데이터 -> 가공하기
# 4. 데이터 프레임 정리
# 5. mysql 연결 / 앱 데이터 베이스와 연결
# 6. 매일 실행되도록 프로그래밍

from selenium.webdriver.chrome.options import Options
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import datetime

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser

# 갑자기 안될 때는 크롬 버전이 달라서 그런 것이므로, 그에 맞는 driver 다운로드하면 된다.
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path='C:\chromedriver', chrome_options=options)


# Every Day, Crawling investors trend
# step 1 - KRX 정보시스템

# 사이트 접속
now = datetime.datetime.now()
crawling_time = now.strftime('%Y/%m/%d')
URL = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203#'
driver.get(url=URL)
sleep(3)

def getVolumeData(corporation, num):
    # 검색창 입력
    driver.find_element_by_xpath('//*[@id="btnisuCd_finder_stkisu0_0"]').click()
    sleep(2)
    search_cor = driver.find_element_by_xpath('//*[@id="searchText__finder_stkisu0_0"]')
    search_cor.send_keys(corporation)
    search_cor.send_keys(Keys.RETURN)
    sleep(2)
    driver.find_element_by_xpath('//*[@id="jsGrid__finder_stkisu0_0"]/tbody/tr[1]').click()
    driver.find_element_by_xpath('//*[@id="jsSearchButton"]').click()
    # Data Crawling
    Price = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[1]/td[1]')
    Count = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[1]/td[2]')
    Foreign_rate = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[4]/td[2]')
    PER_PBR = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[5]/td[2]')
    for i in [Price, Count, Foreign_rate, PER_PBR]:
        data_list.append(i)
    # 이동
    sleep(1)
    if num == 0:
        driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/ul/li[2]/a').send_keys(Keys.ENTER)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="MDCSTAT023_FORM"]/div[1]/div/table/tbody/tr[3]/td[1]/div/div/button[2]').send_keys(Keys.ENTER)
    sleep(2)
    #driver.find_element_by_id('jsSearchButton').click()     # 오류발생
    # 거래내역 뽑기
    # ////
    # 되돌아가기
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)

data_list = []
num = 0
for i in ['삼성전자', '대한항공', 'LG전자']:
    getVolumeData(i, num)
    num += 1
    print(data_list)
    data_list=[]
sleep(10)

driver.quit()


print(data_list)
# step 2 - Naver finance

