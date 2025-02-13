from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # Add this import
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import requests
from selenium.common.exceptions import NoSuchElementException


# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Uncomment if you want to run in headless mode

# Set up the Chrome service
service = Service(executable_path="./driver/chromedriver.exe")

# Initialize the driver with service and options
driver = webdriver.Chrome(service=service, options=chrome_options)


target_account = 'ksu_saac'

def setup_driver():
    chrome_options = Options()
    # Add options to make scraping more reliable
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-notifications')
    
    service = Service(executable_path="./driver/chromedriver.exe")
    return webdriver.Chrome(service=service, options=chrome_options)

try:
    # Navigate to Instagram
    driver.get("https://www.instagram.com/")
    
    # Wait for 5 seconds
    time.sleep(5)
    
    # Updated syntax for finding elements
    username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    
    username.clear()
    password.clear()
    username.send_keys("the_great_escape_2021")
    password.send_keys("Ethansucks21")
    login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    
    time.sleep(5)
    
    #navigate to the target account
    driver.get("https://www.instagram.com/" + target_account )
    
    time.sleep(5)
    
    #find followers button and click it
    followers_a_tag = driver.find_element(By.CSS_SELECTOR, "#mount_0_0_X6 > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div:nth-child(2) > div > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y.x8vgawa > section > main > div > header > section.xc3tme8.x1xdureb.x18wylqe.x13vxnyz.xvxrpd7 > ul > li:nth-child(2) > div > a")
    
    followers_a_tag.click()
    
    #save screenshot for debugging
    driver.save_screenshot("followers.png")
    
    time.sleep(5)
    
    
    
finally:
    # Close the browser
    driver.quit()