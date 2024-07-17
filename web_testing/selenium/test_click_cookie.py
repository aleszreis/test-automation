from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

from selenium.common.exceptions import StaleElementReferenceException

def click_multiple_times(element, clicks):
    while clicks > 0:
        try:
            element.click()
            clicks -= 1
        except StaleElementReferenceException:
            pass
    time.sleep(1)

WEBSITE_PATH = 'https://orteil.dashnet.org/cookieclicker/'

service = Service(executable_path='./chromedriver/chromedriver.exe')
driver = webdriver.Chrome()

driver.get(WEBSITE_PATH)

"""
time.sleep(4)
driver.find_element(By.ID, 'langSelect-EN').click()

time.sleep(12)
driver.find_element(By.ID, 'bigCookie').click()
time.sleep(1)
"""

wait = WebDriverWait(driver, 15)

select_lang = wait.until(EC.presence_of_element_located((By.ID, 'langSelect-EN')))
select_lang.click()

big_cookie = wait.until(EC.presence_of_element_located((By.ID, 'bigCookie')))
click_multiple_times(element=big_cookie, clicks=15)

cookie_count = driver.find_element(By.ID, 'cookies').text.split()[0]
assert cookie_count == "1", "There should be one cookie, but there are " + cookie_count

cps = driver.find_element(By.ID, 'cookiesPerSecond').text
assert cps == "per second: 0", "There shouldn't be any cookies per second, but there are " + cps

driver.quit()