from base_crawling import getVolumeData
from firebase import Check_data
from selenium.webdriver.chrome.options import Options
import selenium
from selenium import webdriver
from time import sleep
import datetime

# input 기업 입력
cor = []
corporation_num = input("원하는 기업의 수를 입력하세요 : ")
for i in range(0, int(corporation_num)):
    corporation = str(input(f"원하는 기업을 입력하세요 ({i+1}/{int(corporation_num)}) : "))
    cor.append(corporation)


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

# crawling
num = 0
for i in cor:
    sleep(1)
    getVolumeData(i, num, driver)
    num += 1
sleep(10)
driver.quit()