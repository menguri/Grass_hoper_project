from firebase import Check_data, get_data
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

print('-----------------------------------------------------------------------------------------------------------------------------------')
data = get_data('삼성전자')
df = pd.DataFrame(data)
df = df.transpose()
print(df)
