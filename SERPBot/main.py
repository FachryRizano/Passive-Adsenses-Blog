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
import random
import urllib
import pydub
import speech_recognition as sr
pydub.AudioSegment.converter = os.getcwd() +"\\ffmpeg.exe"
pydub.AudioSegment.ffprobe = os.getcwd() +"\\ffprobe.exe"

def get_xpath(xpath):
    return WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,xpath)))
def delay ():
    time.sleep(random.randint(2,3))

def init_driver():
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
    return driver

def register_email_to_service(email,password):
    driver.get("https://serpapi.com/users/sign_up")
    
    # Click Sign Up
    get_xpath("/html/body/div[1]/div/div/div[1]/form/div[2]/a[2]").click()
    
    # Gmail
    email_input = get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input')
    email_input.send_keys(email)
    delay()
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    delay()
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(password)
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    
    # Get API Key
    delay()
    driver.get('https://mail.google.com/mail/u/0/#inbox')
    driver.refresh()

    #Get all email box 
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[9]/div/div[1]/div[3]/div/table/tbody/tr')))
        mailbox = WebDriverWait(driver,10).until(lambda driver : driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[9]/div/div[1]/div[3]/div/table/tbody'))
    except:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[3]/div/table/tbody/tr')))
        mailbox = WebDriverWait(driver,10).until(lambda driver : driver.find_element(By.XPATH,'/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[3]/div/table/tbody'))
    mails = WebDriverWait(mailbox,10).until(lambda mailbox : mailbox.find_elements(By.XPATH,'.//tr'))
    
    # Find SERPapi confirmation
    for mail in mails:
        if mail.text.find('no-reply') != -1:
            # print(mail.text)
            break
    driver.execute_script("arguments[0].click()",mail)
    
    # Verify Email
    link = get_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div/p[3]/a')
    link = link.get_attribute('href')
    # delay()
    # driver.switch_to.new_window()
    # link.click()
    # Change tab
    # driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)
    # Subscribe to SERP API
    get_xpath('/html/body/div[1]/div/div/div[1]/form/input[2]').click()
    
    #switch to recaptcha frame
    frames=driver.find_elements(By.TAG_NAME,"iframe")
    for frame in frames:
        if frame.get_attribute('title').find('recaptcha')!=-1:
            break
    driver.switch_to.frame(frame)
    delay()
    get_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button').click()
    delay()
    
    # src = driver.find_element_by_id("audio-source").get_attribute("src")
    src = get_xpath("/html/body/div/div/div[7]/a").get_attribute('href')
    print("[INFO] Audio src: %s"%src)
    delay()
    #download the mp3 audio file from the source
    urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
    delay()
    sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
    sound.export(os.getcwd()+"\\sample.wav", format="wav")
    delay()
    audio_path= os.getcwd()+"\\sample.wav"
    sample_audio = sr.AudioFile(audio_path)
    r = sr.Recognizer()
    with sample_audio as source:
       audio = r.record(source)
    #translate audio to text with google voice recognition
    key=r.recognize_google(audio)
    print("[INFO] Recaptcha Passcode: %s"%key)
    get_xpath('/html/body/div/div/div[6]/input').send_keys(key)
    get_xpath('/html/body/div/div/div[8]/div[2]/div[1]/div[2]/button').click()
    driver.close()

def get_api_key(email,password):
    driver.get("https://serpapi.com/users/sign_in")
    # Click Sign Up
    get_xpath("/html/body/div/div/div/div[2]/form/div[1]/a[2]").click()
    
    # Gmail
    email_input = get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input')
    email_input.send_keys(email)
    delay()
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    delay()
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(password)
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    api_key = get_xpath('/html/body/div[1]/div[2]/main/div/div[2]/div[3]/div/div/input').get_attribute('value')
    return api_key

def change_password(email,old_p,new_p='asdswt123'):

    driver.get('https://accounts.google.com/ServiceLogin/signinchooser?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    email_input = get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input')
    email_input.send_keys(email)
    delay()
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    delay()
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(old_p)
    try:
        get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
        confirm = get_xpath('/html/body/c-wiz[2]/c-wiz/div/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div/span/span')
        driver.execute_script('arguments[0].click()',confirm)
    except:
        pass
    driver.get('https://myaccount.google.com/personal-info')
    change_password = get_xpath('/html/body/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[9]/div/div/div[2]/div/a/div')
    driver.execute_script('arguments[0].click()',change_password)
    
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(old_p)
    get_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    new_password = get_xpath('/html/body/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/form/div/div[1]/div/div[1]/div/div/div/label/input')
    new_password.send_keys(new_p)
    confirm_password = get_xpath('/html/body/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/form/div/div[1]/div/div[3]/div/div/label/input')
    confirm_password.send_keys(new_p)
    submit = get_xpath('/html/body/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/form/div/div[2]/div/div/button/div[3]')
    driver.execute_script('arguments[0].click()',submit)

if __name__ == '__main__':
    # Change password
    df = pd.read_csv('api_data.csv')
    df = df[df['registered'] == False]
    # df = df[~df['api_key'].isna()]
    for i,row in df.iterrows():
        # try:
        while True:
            try:
                driver = init_driver()
                register_email_to_service(row['email'],row['password'])
                print(f"Email :{row['email']}, Done")
                break
            except Exception as e:
                print(e)
                driver.close()
                pass
        # except:
        #     pass
    # time.sleep(600)
    # driver.close()