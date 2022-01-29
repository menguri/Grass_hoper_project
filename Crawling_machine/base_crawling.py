# to do list
# 6. 매일 실행되도록 프로그래밍
from msilib.schema import Class
from firebase import Count_storage

import re
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
import pandas as pd
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser

# Every Day, Crawling investors trend
# step 1 - KRX 정보시스템  

def getVolumeData(corporation, num, driver):
    now = datetime.datetime.now()
    week = datetime.datetime.today().weekday()
    if week == 5 or 6:
        return print("Today is weekend. No Data.")
    crawling_time = now.strftime('%Y%m%d') 
    # 검색창 입력
    driver.find_element_by_xpath('//*[@id="btnisuCd_finder_stkisu0_0"]').click()
    sleep(2)
    search_cor = driver.find_element_by_xpath('//*[@id="searchText__finder_stkisu0_0"]')
    search_cor.send_keys(corporation)
    search_cor.send_keys(Keys.RETURN)
    sleep(2)
    driver.find_element_by_xpath('//*[@id="jsGrid__finder_stkisu0_0"]/tbody/tr[1]').click()
    driver.find_element_by_xpath('//*[@id="jsSearchButton"]').click()
    sleep(10)
    # ----- Data Crawling -----
    Price = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[1]/td[1]').text
    Count = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[1]/td[2]').text
    Foreign_rate = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[4]/td[2]').text
    PER_PBR = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[5]/td[2]').text
    PER, PBR = PER_PBR.split('/')
    # Price = int(re.sub(r"[^a-zA-Z0-9]","", Price))
    # Count = int(re.sub(r"[^a-zA-Z0-9]","", Count))
    # 이동
    sleep(1)
    if num == 0:
        driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/ul/li[2]/a').send_keys(Keys.ENTER)
    sleep(1)
    # ----- 거래내역 뽑기 -----
    # 검색창 입력
    driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/table/tbody/tr[2]/td/div/div/p/img').click()
    sleep(2)
    search_cor = driver.find_element_by_xpath('//*[@id="searchText__finder_stkisu0_1"]')
    search_cor.clear()
    search_cor.send_keys(corporation)
    search_cor.send_keys(Keys.RETURN)
    sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/div[7]/div[2]/div/form/div[2]/a').click()
    sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/div[7]/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]').click()
    sleep(2)
    # 날짜 입력
    start = driver.find_element_by_xpath('//*[@id="strtDd"]')
    start.clear()
    start.send_keys(crawling_time)
    end = driver.find_element_by_xpath('//*[@id="endDd"]')
    end.clear()
    end.send_keys(crawling_time)
    sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/a').click()
    sleep(4)
    html = driver.page_source
    # pip install lxml
    soup = BeautifulSoup(html, 'html.parser')
    table_html = soup.find('table', {'class' : 'CI-GRID-BODY-TABLE'})
    table_html = str(table_html)
    table_df_list = pd.read_html(table_html)
    table_df = table_df_list[0]
    Corpor_count = str(table_df['순매수'][7])
    Personal_count = str(table_df['순매수'][9])
    Foreign_count = str(table_df['순매수'][10])
    # 되돌아가기
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)
    # fin
    dic = {
        'Price': Price,
        'Count': Count,
        'Foreign_rate': Foreign_rate,
        'PER': PER, 
        'PBR': PBR, 
        'Corpor_count': Corpor_count, 
        'Personal_count': Personal_count, 
        'Foreign_count': Foreign_count
    }
    # crawling_df = pd.DataFrame(dic, index=[num])
    Count_storage(dic, corporation, crawling_time)