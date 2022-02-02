from base_crawling import Daily_VolumeData, Period_VolumeData
from firebase import Check_data
from selenium.webdriver.chrome.options import Options
import selenium
from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta
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

# 갑자기 안될 때는 크롬 버전이 달라서 그런 것이므로, 그에 맞는 driver 다운로드하면 된다.
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("start-maximized")
options.add_argument("--disable-software-rasterizer")
driver = webdriver.Chrome(executable_path='C:\chromedriver', chrome_options=options)
URL = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203#'
driver.get(url=URL)

num = 0
sleep(1)
if num == 0:
    driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)
sleep(1)
driver.find_element_by_xpath('//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/ul/li[2]/a').send_keys(Keys.ENTER)

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
# search_cor.send_keys('삼성전자')
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
start.send_keys('20220124')
sleep(1)
end = driver.find_element_by_xpath('//*[@id="endCalendar"]')
end.clear()
end.send_keys('20220124')
driver.find_element_by_xpath('//*[@id="jsSearchButton"]').click()
sleep(8)
per_html = driver.page_source
soup = BeautifulSoup(per_html, 'html.parser')
table_html = soup.find_all('table', {'class' : 'CI-GRID-BODY-TABLE'})
table_html = str(table_html)
table_df_list = pd.read_html(table_html)
print(table_df_list)
table_df = table_df_list[1]
print(table_df)
PER = str(table_df['PER'][0])
PBR = str(table_df['PBR'][0])
Price = str(table_df['종가'][0])


# driver.quit()