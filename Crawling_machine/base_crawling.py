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
# step 1. Daily 수집

def Daily_VolumeData(corporation, num, driver, time, dates):
    week = datetime.date(time[0], time[1], time[2]).weekday()
    if week == 5 :
        return print("Today is weekend. No Data.")
    elif week == 6 :
        return print("Today is weekend. No Data.")
    # 검색창 입력
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="btnisuCd_finder_stkisu0_0"]'))).click()
    sleep(2)
    search_cor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchText__finder_stkisu0_0"]')))
    search_cor.send_keys(corporation)
    search_cor.send_keys(Keys.RETURN)
    sleep(3)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jsGrid__finder_stkisu0_0"]/tbody/tr[1]/td[1]'))).click()
    sleep(2)
    driver.find_element_by_xpath('//*[@id="jsSearchButton"]').click()
    sleep(8)
    # ----- Data Crawling -----
    Price = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[1]/td[1]').text
    Count = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[1]/td[2]').text
    Foreign_rate = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[4]/td[2]').text
    PER_PBR = driver.find_element_by_xpath('//*[@id="isuInfoBind"]/table/tbody/tr[5]/td[2]').text
    PER, PBR = PER_PBR.split('/')
    # Price = int(re.sub(r"[^a-zA-Z0-9]","", Price))
    # Count = int(re.sub(r"[^a-zA-Z0-9]","", Count))
    # 이동
    if num == 0:
        driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/ul/li[2]/a').send_keys(Keys.ENTER)
    # ----- 거래내역 뽑기 -----
    # 검색창 입력
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/table/tbody/tr[2]/td/div/div/p/img'))).click()
    search_cor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchText__finder_stkisu0_1"]')))
    search_cor.clear()
    search_cor.send_keys(corporation)
    search_cor.send_keys(Keys.RETURN)
    sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/div[7]/div[2]/div/form/div[2]/a').click()
    sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/div[7]/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]').click()
    sleep(2)
    # 날짜 입력
    start = driver.find_element_by_xpath('//*[@id="strtDd"]')
    start.clear()
    start.send_keys(dates)
    sleep(1)
    end = driver.find_element_by_xpath('//*[@id="endDd"]')
    end.clear()
    end.send_keys(dates)
    sleep(1)
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
        'Foreign_count': Foreign_count,
        'week': str(week)
    }
    # crawling_df = pd.DataFrame(dic, index=[num])
    Count_storage(dic, corporation, dates)



# step 2. 원하는 기간만큼 데이터 수집

def Period_VolumeData(corporation, num, driver, time, dates):
    week = datetime.date(time[0], time[1], time[2]).weekday()
    if week == 5 :
        return print("Today is weekend. No Data.")
    elif week == 6 :
        return print("Today is weekend. No Data.")
    # 기업 바뀔 때마다 새로고침
    if num == 0 :
        driver.refresh()
    # [투자자별 실적 거래] 이동  --------------------------------------------------------------------------------------------------------------------
    sleep(5)
    if num == 0:
        driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/ul/li[2]/a').send_keys(Keys.ENTER)
    # ----- 거래내역 뽑기 -----
    # 검색창 입력
    if num == 0:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/table/tbody/tr[2]/td/div/div/p/img'))).click()
        search_cor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/div[7]/div[2]/div/form/div[2]/input[1]')))
        search_cor.clear()
        search_cor.send_keys(corporation)
        search_cor.send_keys(Keys.RETURN)
        sleep(3)
        driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/div[7]/div[2]/div/form/div[2]/a').click()
        sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/div[7]/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]').click()
    sleep(2)
    # 날짜 입력
    start = driver.find_element_by_xpath('//*[@id="strtDd"]')
    start.clear()
    start.send_keys(dates)
    end = driver.find_element_by_xpath('//*[@id="endDd"]')
    end.clear()
    end.send_keys(dates)
    driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/a').click()
    sleep(4)
    html = driver.page_source
    # pip install lxml
    soup = BeautifulSoup(html, 'html.parser')
    table_html = soup.find('table', {'class' : 'CI-GRID-BODY-TABLE'})
    table_html = str(table_html)
    table_df_list = pd.read_html(table_html)
    table_df = table_df_list[0]
    Count = str(table_df['매수'][12])
    Corpor_count = str(table_df['순매수'][7])
    Personal_count = str(table_df['순매수'][9])
    Foreign_count = str(table_df['순매수'][10])
    # [PER/PBR 개별 종목] 이동  --------------------------------------------------------------------------------------------------------------------
    if num == 0:
        driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/a').send_keys(Keys.ENTER)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/ul/li[2]/a').send_keys(Keys.ENTER)
    sleep(2)
    driver.find_element_by_xpath('//*[@id="MDCSTAT035_FORM"]/div[2]/div/table/tbody/tr[1]/td/label[2]').click()
    sleep(2)
    # driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[3]/form/div[2]/div/table/tbody/tr[4]/td/div/div/p/img').click()
    # # 검색항목 입력
    # search_cor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[3]/div[4]/div[2]/div/form/div[2]/input[1]')))
    # search_cor.clear()
    # search_cor.send_keys(corporation)
    # search_cor.send_keys(Keys.RETURN)
    # sleep(3)
    # driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[3]/div[4]/div[2]/div/form/div[2]/a').click()
    # sleep(2)
    # driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[3]/div[4]/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]').click()
    # sleep(2)
    # 이전 창들 제거
    driver.find_element_by_xpath('//*[@id="jsMdiTab"]/li[2]/a/button').click()
    driver.find_element_by_xpath('//*[@id="jsMdiTab"]/li[1]/a/button').click()
    # 날짜 입력
    start = driver.find_element_by_xpath('//*[@id="startCalender"]')
    start.clear()
    start.send_keys(dates)
    sleep(1)
    end = driver.find_element_by_xpath('//*[@id="endCalendar"]')
    end.clear()
    end.send_keys(dates)
    driver.find_element_by_xpath('//*[@id="jsSearchButton"]').click()
    sleep(4)
    per_html = driver.page_source
    soup = BeautifulSoup(per_html, 'html.parser')
    table_html = soup.find_all('table', {'class' : 'CI-GRID-BODY-TABLE'})
    table_html = str(table_html)
    table_df_list = pd.read_html(table_html)
    table_df = table_df_list[1]
    print(table_df)
    PER = str(table_df['PER'][0])
    PBR = str(table_df['PBR'][0])
    Price = str(table_df['종가'][0])
    # [외국인 보유량 개별종목] 이동  --------------------------------------------------------------------------------------------------------------------
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/ul/li[4]/a').send_keys(Keys.ENTER)
    sleep(1)
    # 이전 창 삭제
    driver.find_element_by_xpath('//*[@id="jsMdiTab"]/li[1]/a/button').click()
    # 검색 시작
    driver.find_element_by_xpath('//*[@id="MDCSTAT037_FORM"]/div[2]/div/table/tbody/tr[1]/td/label[2]').click()
    sleep(2)
    # driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div/table/tbody/tr[4]/td/div/div/p/img').click()
    # # 검색항목 입력
    # search_cor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div/div[4]/div[2]/div/form/div[2]/input[1]')))
    # search_cor.clear()
    # search_cor.send_keys(corporation)
    # search_cor.send_keys(Keys.RETURN)
    # sleep(3)
    # driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div/div[4]/div[2]/div/form/div[2]/a').click()
    # sleep(2)
    # driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div/div[4]/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]').click()
    # sleep(2)
    # 날짜 입력
    start = driver.find_element_by_xpath('//*[@id="startCalender"]')
    start.clear()
    start.send_keys(dates)
    sleep(1)
    end = driver.find_element_by_xpath('//*[@id="endCalendar"]')
    end.clear()
    end.send_keys(dates)
    driver.find_element_by_xpath('//*[@id="jsSearchButton"]').click()
    sleep(4)
    foreign_html = driver.page_source
    soup = BeautifulSoup(foreign_html, 'html.parser')
    table_html = soup.find_all('table', {'class' : 'CI-GRID-BODY-TABLE'})
    table_html = str(table_html)
    table_df_list = pd.read_html(table_html)
    table_df = table_df_list[1]
    print(table_df)
    Foreign_rate = str(table_df['외국인지분율'][0])
    # 되돌아가기
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)
    # 이전 창 삭제
    driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/ul/li[1]/a/button').click()
    # fin
    dic = {
        'Price': Price,
        'Count': Count,
        'Foreign_rate': Foreign_rate,
        'PER': PER, 
        'PBR': PBR, 
        'Corpor_count': Corpor_count, 
        'Personal_count': Personal_count, 
        'Foreign_count': Foreign_count,
        'week': str(week)
    }
    # crawling_df = pd.DataFrame(dic, index=[num])
    Count_storage(dic, corporation, dates)