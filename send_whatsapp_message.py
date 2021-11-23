from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

WhatAppGroupID = "PUT_HERE_THE_GROUP_ID"

MiddleEastNine_txt = "Market Open - Middle East Markets opening - Was successful"
JSE_txt = "Market Open - JSE-DEC21 - was successful"
MiddleEastTen_txt = "Market Open - Middle East Markets opening was successful (TADAWUL, SABIC, STC, ARAMCO)"
Europe_txt = "Market Open - Europe was successful"
SUG11_txt = "Market open - Future Commodities check (SUG11-MAR22) - was successful"
COFFEE_txt = "Market open - Future Commodities check (COFFE-DEC21) - was successful"
COCOA_txt = "Market open - Future Commodities check (COCOA-DEC21) - was successful"
ORANGE_txt = "Market open - Future Commodities check (ORANG-NOV21) - was successful"
UsMarket_txt = "Market open - US Markets check - was successful"


def send_message(txt):
    currentPath = os.path.dirname(os.path.realpath(__file__))
    driverPath = currentPath + "\chromedriver.exe"
    # currentPath = os.getcwd()
    # driverPath = currentPath + "\chromedriver.exe"
    s = Service(driverPath)

    # Using Chrome Driver Manager for driver
    # s = Service(ChromeDriverManager(version="95.0.4638.69").install())

    # Options
    chromeOptions = Options()
    chromeOptions.add_argument("user-data-dir=" + currentPath + "cookies")  # Save Cookies to not login each time to WhatsApp Web
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Open the browser in the background
    chromeOptions.add_argument('headless')
    chromeOptions.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, "
                               "like Gecko) Chrome/65.0.3312.0 Safari/537.36")
    chromeOptions.add_argument("remote-debugging-port=3333")

    driver = webdriver.Chrome(service=s, options=chromeOptions, service_log_path=None)

    # Open URL
    driver.get(f"https://web.whatsapp.com/accept?code={WhatAppGroupID}")

    print("Loading Page")
    time.sleep(30)
    textBox = driver.find_element(By.CLASS_NAME, "p3_M1")
    print("Page Loaded")

    # Text content
    textBox.click()
    textBox.send_keys(txt)
    time.sleep(20)

    # Send Message
    sendButton = driver.find_element(By.CLASS_NAME, "_4sWnG")
    time.sleep(10)
    sendButton.click()

    print("Message Sent")
    time.sleep(10)
    driver.close()


if __name__ == '__main__':
    send_message("TEST2")
