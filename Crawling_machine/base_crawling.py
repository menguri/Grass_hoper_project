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



class crawling_corporation:
    def __init__(self) -> None:
        pass

    # 첫 단계
    def step1(self, corporation, driver, num, week, dates):
        # 진입
        if num == 0:
            sleep(3)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/a').send_keys(Keys.ENTER)
            sleep(2)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[3]/ul/li[2]/a').send_keys(Keys.ENTER)
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
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/div[7]/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]'))).click()
        sleep(2)
        # 날짜 입력
        end = driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/table/tbody/tr[3]/td[1]/div/div/input[2]')
        end.clear()
        end.send_keys(dates)
        sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/table/tbody/tr[3]/td[1]/div/div/button[2]'))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/a'))).click()
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
        # fin
        dic = {
            'Date': dates,
            'Count': Count,
            'Corpor_count': Corpor_count, 
            'Personal_count': Personal_count, 
            'Foreign_count': Foreign_count,
            'week': str(week)
        }
        return dic

    # 두번째 단계
    def step2(self, corporation, driver, num, week, dates):
        if num == 0:
            sleep(4)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/a').send_keys(Keys.ENTER)
            sleep(1)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/ul/li[2]/a').send_keys(Keys.ENTER)
            sleep(2)
            driver.find_element_by_xpath('//*[@id="MDCSTAT035_FORM"]/div[2]/div/table/tbody/tr[1]/td/label[2]').click()
        # 검색창 입력
        if num == 0:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[2]/div/table/tbody/tr[4]/td/div/div/p/img'))).click()
            search_cor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/div[4]/div[2]/div/form/div[2]/input[1]')))
            search_cor.clear()
            search_cor.send_keys(corporation)
            search_cor.send_keys(Keys.RETURN)
            sleep(3)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/div[4]/div[2]/div/form/div[2]/a').click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/div[4]/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]'))).click()
        sleep(2)
        # 날짜 입력
        end = driver.find_element_by_xpath('//*[@id="endCalendar"]')
        end.clear()
        end.send_keys(dates)
        sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[2]/div/table/tbody/tr[5]/td/div/div/button[2]'))).click()
        driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[2]/div/a').click()
        sleep(4)
        per_html = driver.page_source
        soup = BeautifulSoup(per_html, 'html.parser')
        table_html = soup.find_all('table', {'class' : 'CI-GRID-BODY-TABLE'})
        table_html = str(table_html)
        table_df_list = pd.read_html(table_html)
        table_df = table_df_list[1]
        PER = str(table_df['PER'][0])
        PBR = str(table_df['PBR'][0])
        Price = str(table_df['종가'][0]) 
        #fin
        dic = {
            'Date': dates,
            'Price': Price,
            'PER': PER, 
            'PBR': PBR, 
        }       
        return dic
    
    # 세번째 단계
    def step3(self, corporation, driver, num, week, dates):
        if num == 0:
            sleep(4)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/a').send_keys(Keys.ENTER)
            sleep(1)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/ul/li[4]/a').send_keys(Keys.ENTER)
            sleep(2)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[2]/div/table/tbody/tr[1]/td/label[2]').click()
        # 검색창 입력
        if num == 0:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[2]/div/table/tbody/tr[4]/td/div/div/p/img'))).click()
            search_cor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/div[4]/div[2]/div/form/div[2]/input[1]')))
            search_cor.clear()
            search_cor.send_keys(corporation)
            search_cor.send_keys(Keys.RETURN)
            sleep(3)
            driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/div[4]/div[2]/div/form/div[2]/a').click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/div[4]/div[2]/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]'))).click()
        sleep(2)
        # 날짜 입력
        end = driver.find_element_by_xpath('//*[@id="endCalendar"]')
        end.clear()
        end.send_keys(dates)
        sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[2]/div/table/tbody/tr[5]/td/div/div/button[2]'))).click()
        driver.find_element_by_xpath('/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[2]/div/a').click()
        sleep(4)
        # 페이지 크롤링
        foreign_html = driver.page_source
        soup = BeautifulSoup(foreign_html, 'html.parser')
        table_html = soup.find_all('table', {'class' : 'CI-GRID-BODY-TABLE'})
        table_html = str(table_html)
        table_df_list = pd.read_html(table_html)
        table_df = table_df_list[1]
        Foreign_rate = str(table_df['외국인지분율'][0])
        # fin
        dic = {
            'Date': dates,
            'Foreign_rate': Foreign_rate,
        }
        return dic
    
    def summary():
        return 0