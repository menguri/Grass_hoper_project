# selenium

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

URL = 'https://finance.naver.com/'

# 갑자기 안될 때는 크롬 버전이 달라서 그런 것이므로, 그에 맞는 driver 다운로드하면 된다.
driver = webdriver.Chrome(executable_path='C:\chromedriver')
driver.get(url=URL)

sleep(10)

driver.quit()

# haha



