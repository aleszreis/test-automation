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
wait = WebDriverWait(driver, 15)

# Select language
select_lang = wait.until(EC.presence_of_element_located((By.ID, 'langSelect-EN')))
select_lang.click()

# Find cursor and check that is blocked
cursor = wait.until(EC.presence_of_element_located((By.ID, 'product0')))
cursor_classes = cursor.get_attribute('class')
assert 'locked' in cursor_classes, "Product should be locked but it isn't." + print(cursor_classes)
assert 'disabled' in cursor_classes, "Product should be disabled but it isn't." + print(cursor_classes)

time.sleep(2)
# Find and click on big cookie 10 times
big_cookie = wait.until(EC.presence_of_element_located((By.ID, 'bigCookie')))
click_multiple_times(element=big_cookie, clicks=10)

time.sleep(2)
# Check that cursor is still blocked
cursor = wait.until(EC.presence_of_element_located((By.ID, 'product0')))
cursor_classes = cursor.get_attribute('class')
assert 'locked' in cursor_classes, "Product should be locked but it isn't." + print(cursor_classes)
assert 'disabled' in cursor_classes, "Product should be disabled but it isn't." + print(cursor_classes)

time.sleep(2)
# Find and click on big cookie 5 more times
click_multiple_times(element=big_cookie, clicks=5)

time.sleep(2)
# Check that cursor is unlocked and enabled
cursor = wait.until(EC.presence_of_element_located((By.ID, 'product0')))
cursor_classes = cursor.get_attribute('class')
assert 'unlocked' in cursor_classes, "Product shouldn't be locked but it is. " + print(cursor_classes)
assert 'enabled' in cursor_classes, "Product shouldn't be disabled but it is." + print(cursor_classes)

time.sleep(2)
# Buy one cursor
cursor.click()

time.sleep(2)
# Assert that cursor is unlocked but disabled
cursor = wait.until(EC.presence_of_element_located((By.ID, 'product0')))
cursor_classes = cursor.get_attribute('class')
assert 'unlocked' in cursor_classes, "Product should be unlocked but it isn't." + print(cursor_classes)
assert 'disabled' in cursor_classes, "Product should be disabled but it isn't." + print(cursor_classes)

time.sleep(2)
# Assert that cookie count and cps were altered
cookie_count = driver.find_element(By.ID, 'cookies').text.split()[0]
assert cookie_count == 0, f"There should be 0 cookie, but there are " + cookie_count

cps = driver.find_element(By.ID, 'cookiesPerSecond').text
assert cps == "per second: 0.1", "There should be 0.1 cookies per second, but there are " + cps

time.sleep(20)
# Close
driver.quit()