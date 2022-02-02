from base_crawling import Daily_VolumeData, Period_VolumeData
from firebase import Check_data
from selenium.webdriver.chrome.options import Options
import selenium
from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta

# input 기업 입력
cor = []
corporation_num = input("원하는 기업의 수를 입력하세요 : ")
for i in range(0, int(corporation_num)):
    corporation = str(input(f"원하는 기업을 입력하세요 ({i+1}/{int(corporation_num)}) : "))
    cor.append(corporation)

# time 선택
start = str(input("시작 시점을 입력하세요. ex) 2021-08-01 : "))
finish = str(input("종료 시점을 입력하세요. ex) 2021-08-01 : "))
start_date = datetime.strptime(start, "%Y-%m-%d") 
last_date = datetime.strptime(finish, "%Y-%m-%d") 

# mode 선택
mode = str(input("Daily or Period : "))

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

# Crawling 진행
for i in cor:
    num = 0
    start = start_date
    last = last_date
    while start <= last: 
        dates = start.strftime("%Y%m%d") 
        time = [int(dates[0:4]), int(dates[4:6]), int(dates[6:8])]
        start += timedelta(days=1)
        if mode == 'Period':
            Period_VolumeData(i, num, driver, time, dates)
        else:
            Daily_VolumeData(i, num, driver, time, dates)
        num += 1
sleep(10)
driver.quit()


#   PER, 외국인 표에서 자꾸 다른 기업들이 모두 뜬다. 해결 방법 찾을 것.
