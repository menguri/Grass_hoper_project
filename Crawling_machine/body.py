from turtle import pd
from base_crawling import crawling_corporation
from firebase import Check_data
from selenium.webdriver.chrome.options import Options
import selenium
from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta, date
import pandas as pd
from firebase import Count_storage
import time
import datetime
import math

# input 기업 입력
cor = []
corporation_num = input("원하는 기업의 수를 입력하세요 : ")
for i in range(0, int(corporation_num)):
    corporation = str(input(f"원하는 기업을 입력하세요 ({i+1}/{int(corporation_num)}) : "))
    cor.append(corporation)

# time 선택
start = str(input("시작 시점을 입력하세요(주말X). ex) 2021-08-01 : "))
finish = str(input("종료 시점을 입력하세요. ex) 2021-08-01 : "))
start_date = datetime.strptime(start, "%Y-%m-%d") 
last_date = datetime.strptime(finish, "%Y-%m-%d") 

# 갑자기 안될 때는 크롬 버전이 달라서 그런 것이므로, 그에 맞는 driver 다운로드하면 된다.
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("start-maximized")
options.add_argument("--disable-software-rasterizer")
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome(executable_path='C:\chromedriver.exe', chrome_options=options)
URL = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203#'



# Crawling 진행
# 시간 측정
start_time = time.time() 
math.factorial(1234567) 
# 시작
crawl_corporation = crawling_corporation()
for corporation in cor:
    print(f'----------------------Corporation is {corporation}----------------------')
    # Dataframe
    step1_df = pd.DataFrame()
    step2_df = pd.DataFrame()
    step3_df = pd.DataFrame()
    for step_number in ['step1', 'step2', 'step3']:
        driver = webdriver.Chrome(executable_path='C:\chromedriver.exe', chrome_options=options)
        driver.get(url=URL)
        start = start_date
        last = last_date
        num = 0
        # 시간 반복
        while start <= last: 
            dates = start.strftime("%Y%m%d") 
            time = [int(dates[0:4]), int(dates[4:6]), int(dates[6:8])]
            week = date(time[0], time[1], time[2]).weekday()   
            # weekend 일 경우
            if week in [5,6] :
                print("Today is weekend. No Data.")
            else:
                if step_number == 'step1':
                    dic = crawl_corporation.step1(corporation, driver, num, week, dates)
                    step1_dic = pd.DataFrame([dic])
                    step1_df = pd.concat([step1_df, step1_dic])
                    num += 1
                elif step_number == 'step2':
                    dic = crawl_corporation.step2(corporation, driver, num, week, dates)
                    step2_dic = pd.DataFrame([dic])
                    step2_df = pd.concat([step2_df, step2_dic])
                    num += 1                   
                else:
                    dic = crawl_corporation.step3(corporation, driver, num, week, dates)
                    step3_dic = pd.DataFrame([dic])
                    step3_df = pd.concat([step3_df, step3_dic])
                    num += 1
            start += timedelta(days=1)
        driver.close()
        print(f'----------------------{step_number} is finished----------------------')
    # final dataframe 정리
    final_df = pd.merge(left = step1_df , right = step2_df, how = "inner", on = "Date")
    final_df = pd.merge(left = final_df , right = step3_df, how = "inner", on = "Date")
    row = final_df['Date'].copy()
    for row_dict in final_df.to_dict(orient="records"):
        time = row_dict['Date']
        Count_storage(row_dict, corporation, time)
# 코드 종료
end_time = time.time()
sec = (end_time - start_time) 
result = datetime.timedelta(seconds=sec) 
print(f'Start Time : {start_time}')
print(f'End Time : {end_time}')
print(f"Running Time : {result}")

sleep(10)
driver.quit()
print('--------------------------------------------Crawling is completed--------------------------------------------')
