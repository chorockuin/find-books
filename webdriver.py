import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# https://sites.google.com/chromium.org/driver/downloads
# https://googlechromelabs.github.io/chrome-for-testing/

def open_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # 현재 설치된 크롬 브라우저에 맞는 드라이버를 설정해야 한다
    service = Service('chromedriver-win64/chromedriver.exe')
    chrome = webdriver.Chrome(service=service, options=chrome_options)
    return chrome

def close_chrome(chrome):
    chrome.quit()

def wait(chrome, xpath):
    WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))