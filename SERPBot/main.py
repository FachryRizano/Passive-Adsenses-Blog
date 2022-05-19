from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os 
import re
import undetected_chromedriver.v2 as uc
import time

def get_xpath(xpath):
    return WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,xpath)))

if __name__ == '__main__':
    # Setting Chrome Driver
    options = uc.ChromeOptions()
    options.add_argument('--log-level=3')
    # options.add_argument('--user-data-dir=hash')
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("--disable-dev-shm-usage")
    # Headless Chrome
    # options.add_argument('--headless')
    driver = uc.Chrome()
    # driver = webdriver.Chrome("chromedriver.exe",options=options)
    data = pd.read_csv('api_data.csv')
    data = data[~data['api_key'].isna()]
    driver.get("https://serpapi.com/users/sign_up")
    # Click Sign Up
    get_xpath("/html/body/div[1]/div/div/div[1]/form/div[2]/a[2]").click()
    # Gmail
    email_input = get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input')
    email_input.send_keys('Renisatina@gmail.com')
    time.sleep(1)
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    time.sleep(1)
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys('asdswt123')
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    # Get API Key
    # api = get_xpath('/html/body/div[1]/div[2]/main/div/div[2]/div[2]/div/div/input').get_attribute('value')
    # Open GMAIL
    time.sleep(1)
    driver.get('https://mail.google.com/mail/u/0/#inbox')
    driver.refresh()
    # print(api)
    time.sleep(600)
    # driver.close()