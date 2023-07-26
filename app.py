#!/usr/bin/python3
### Maintained by carias@redhat.com
import time, os.path, logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

from selenium import webdriver


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

options = webdriver.FirefoxOptions()
options.set_preference("permissions.default.microphone", True)
options.set_capability('browserName', 'firefox')
driver = webdriver.Remote(
   command_executor='http://standalone-firefox-ui-lx-snow.apps.tools-na100.dev.ole.redhat.com/wd/hub',
   options=options)

def intercom_login():
    logging.info("Intercom login")
    try:
        driver.get("https://app.intercom.com/a/inbox/jeuow7ss/inbox/admin/4643910?view=List")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@class="m__login__form"]//*[contains(text(), "Sign in with Google")]'))).click()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierId"]'))).send_keys("carias" + "@redhat.com")
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[contains(text(), "Next")]'))).click()
        except:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]/div[2]'))).click()

        # RH SSO
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(
            "carias")
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(
            str(os.environ.get('SSO-PIN')).replace('\n', '') + str(os.popen("curl -sL https://sso-rh-login-lx-snow.apps.tools-na100.dev.ole.redhat.com/get_otp").read()).replace(
                '\n', ''))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]'))).click()
    except:
        logging.error("An exception occurred while accepting during login")


def skype_login():
    logging.info("Skype login")
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get('https://web.skype.com/')
        # Introduce username
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]'))).send_keys(os.environ.get('SKYPE_USERNAME'))
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/div/div[4]/div/div/div/div/input'))).click()

        # Introduce password
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input'))).send_keys(os.environ.get('SKYPE_PASSWORD'))
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[4]/div[2]/div/div/div/div/input'))).click()

        # Check box to skip another login
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div[1]/div/label/input'))).click()
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input'))).click()

        # Click on notification and  tutorial pop-ups
        click_popups()
        driver.switch_to.window(driver.window_handles[0])
    except:
        logging.error("Skype login failed")
        driver.switch_to.window(driver.window_handles[0])

def click_popups():
    # Click on notification and  tutorial pop-ups
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div[3]/button'))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/button'))).click()


def skype_call():
    try:
        driver.switch_to.window(driver.window_handles[1])
        # Make the call
        logging.info("Calling")
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div[1]/div[3]/div[2]/div[1]/div/div[1]/div/div/div[3]/div[3]/div/div/div[2]/div[1]'))).click()
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/button'))).click()
        # Do it without video or audio
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[1]/div[3]/div[3]/div/div/div/div[2]/div[2]/div/button'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/button'))).click()
        except:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/button'))).click()
            pass
        # Wait for the hang_up
        time.sleep(10)
        logging.info("Ended call")
        driver.switch_to.window(driver.window_handles[0])
    except:
        logging.error("Call failed")
        driver.switch_to.window(driver.window_handles[0])

def wait_for_expert_chat():
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div[1]//*[contains(text(), "Expert") or contains(text(), "@T2")]'))).text
        customer_name = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[3]/div/div[1]/div/div[4]/ul/div/div/li/a/div[2]/div[1]/div[1]'))).text
    except:
        return ''
        pass
    return customer_name


# Main

logging.info("Starting selenium script")
intercom_login()
skype_login()
customer_name = ''
new_customer_name = ''

while True:
    try:
        new_customer = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[3]/div/div[1]/div/div[4]/ul/div/div/li/a/div[2]/div[1]/div[1]')))
        new_customer.click()
        new_customer_name = new_customer.text
    except:
        pass

    if customer_name != new_customer_name:
        logging.info("New chat from: " + new_customer_name)
        customer_name = wait_for_expert_chat()
        skype_call()
    driver.get("https://app.intercom.com/a/inbox/jeuow7ss/inbox/admin/4643910?view=List")
    time.sleep(20)
