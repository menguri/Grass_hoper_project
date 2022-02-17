from base_crawling import Daily_VolumeData, Period_VolumeData, crawling_corporation
from firebase import Check_data
from selenium.webdriver.chrome.options import Options
import selenium
from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta, date

# input 기업 입력
cor = []
# corporation_num = input("원하는 기업의 수를 입력하세요 : ")
corporation_num = 2
# for i in range(0, int(corporation_num)):
#     corporation = str(input(f"원하는 기업을 입력하세요 ({i+1}/{int(corporation_num)}) : "))
#     cor.append(corporation)
cor = ['삼성전자', '카카오']

# time 선택
# start = str(input("시작 시점을 입력하세요(주말X). ex) 2021-08-01 : "))
# finish = str(input("종료 시점을 입력하세요. ex) 2021-08-01 : "))
start = '2022-02-08'
finish = '2022-02-09'
start_date = datetime.strptime(start, "%Y-%m-%d") 
last_date = datetime.strptime(finish, "%Y-%m-%d") 

# mode 선택
# mode = str(input("Daily or Period : "))

# 갑자기 안될 때는 크롬 버전이 달라서 그런 것이므로, 그에 맞는 driver 다운로드하면 된다.
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("start-maximized")
options.add_argument("--disable-software-rasterizer")
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
driver = webdriver.Chrome(executable_path='C:\chromedriver.exe', chrome_options=options)
URL = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203#'

# Crawling 진행

# # Crawling 시작
# for i in cor:
#     num = 0
#     start = start_date
#     last = last_date
#     while start <= last: 
#         dates = start.strftime("%Y%m%d") 
#         time = [int(dates[0:4]), int(dates[4:6]), int(dates[6:8])]
#         week = date(time[0], time[1], time[2]).weekday()
#         # 중간 쉬어주기
#         if num == 10:
#             driver.close()
#             sleep(10)
#             driver = webdriver.Chrome(executable_path='C:\chromedriver', chrome_options=options)
#             URL = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203#'
#             driver.get(url=URL)
#             num = 0
#         # weekend 일 경우, 뛰어넘어버려
#         if week == 5 and 6 :
#             print("Today is weekend. No Data.")
#         else:
#             if mode == 'Period':
#                 Period_VolumeData(i, num, driver, week, dates)
#                 num += 1
#             else:
#                 Daily_VolumeData(i, num, driver, week, dates)
#                 num += 1
#         start += timedelta(days=1)


crawl_corporation = crawling_corporation()
for corporation in cor:
    print(f'----------------------Corporation is {corporation}----------------------')
    for step_number in ['step1', 'step2', 'step3']:
        driver = webdriver.Chrome(executable_path='C:\chromedriver.exe', chrome_options=options)
        driver.get(url=URL)
        start = start_date
        last = last_date
        num = 0
        while start <= last: 
            dates = start.strftime("%Y%m%d") 
            time = [int(dates[0:4]), int(dates[4:6]), int(dates[6:8])]
            week = date(time[0], time[1], time[2]).weekday()   
            # weekend 일 경우
            if week == 5 and 6 :
                print("Today is weekend. No Data.")
            else:
                if step_number == 'step1':
                    dic = crawl_corporation.step1(corporation, driver, num, week, dates)
                    print(dic)
                    num += 1
                elif step_number == 'step2':
                    dic = crawl_corporation.step2(corporation, driver, num, week, dates)
                    print(dic)
                    num += 1                   
                else:
                    dic = crawl_corporation.step3(corporation, driver, num, week, dates)
                    print(dic)
                    num += 1
            start += timedelta(days=1)
        driver.close()
        print(f'----------------------{step_number} is finished----------------------')
sleep(10)
driver.quit()
print('--------------------------------------------Crawling is completed--------------------------------------------')
