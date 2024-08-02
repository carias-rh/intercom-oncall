#!/usr/bin/python3
### Maintained by carias@redhat.com
import time, os.path, logging, sys, traceback, re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium import webdriver


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

options = webdriver.FirefoxOptions()
options.set_preference("permissions.default.microphone", True)
options.set_capability('browserName', 'firefox')
driver = webdriver.Remote(command_executor=str(os.environ.get('SELENIUM_GRID_OPENSHIT_ROUTE')) + "/wd/hub", options=options)
driver.get("https://app.intercom.com/a/inbox/jeuow7ss/inbox/admin/4643910?view=List")

def handle_exception(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_details = traceback.extract_tb(exc_traceback)

    first_function_filename = traceback_details[0].filename
    first_function_line_number = traceback_details[0].lineno
    first_function_name = traceback_details[0].name

    print(
        f"Exception first caught in file {first_function_filename}, line {first_function_line_number}, in {first_function_name}")

    filename = traceback_details[-1].filename
    line_number = traceback_details[-1].lineno
    function_name = traceback_details[-1].name

    print(f"Exception occurred in file {filename}, line {line_number}, in {function_name}")
    print(f"Exception message: {str(e)}")

def intercom_login():
    logging.info("Intercom login")
    try:
        driver.get("https://app.intercom.com/a/inbox/jeuow7ss/inbox/admin/4643910?view=List")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@class="m__login__form"]//*[contains(text(), "Sign in with Google")]'))).click()
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierId"]'))).send_keys("carias" + "@redhat.com")
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Next")]'))).click()
        except:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]/div[2]'))).click()

        # RH SSO
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys("carias")
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(str(os.environ.get('SSO_PIN')).replace('\n', '') + str(os.popen("curl -sL " + str(os.environ.get('SSO_LOGIN_OPENSHIFT_ROUTE')) + "/get_otp").read()).replace('\n', ''))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]'))).click()
        time.sleep(5)
    except Exception as e:
        logging.error("An exception occurred while accepting during login")
        handle_exception(e)

def intercom_change_status(change_status_to):
    logging.info(f"Change intercom status to {change_status_to}")
    try:
        avatar = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div[5]/div/div/div')))
        avatar.click()
        status_raw = avatar.get_attribute(
            "class")
    except:
        avatar = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div[5]/div[2]/div/div')))
        avatar.click()
        status_raw = avatar.get_attribute(
            "class")

    # Get attributes from the gravatar
    status_away = re.findall("o__away", status_raw)
    status_active = re.findall("o__active", status_raw)
    time.sleep(1)
    try:
        # Change status to Away if actual status is active
        if change_status_to == "Away" and status_active:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/button/span'))).click()

            # Reason "Done for the day"
            time.sleep(1)
            avatar.click()
            reason = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/div[4]/div/div[1]/div/div[1]')))
            actions.move_to_element(reason).perform()
            done_for_the_day = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/div[4]/div/div[2]/div/div/div/div[7]')))
            actions.move_to_element(done_for_the_day).click().perform()

            # Reassign replies
            time.sleep(1)
            avatar.click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/div[3]/div/div/button'))).click()

        # Change status to Active if actual status is Away
        if change_status_to == "Active" and status_away:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/button/span'))).click()
    except:
        print("Failed to change intercom status")


def skype_login():
    logging.info("Skype login")
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get('https://web.skype.com/')

        # Introduce username
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@name="loginfmt"]'))).send_keys(os.environ.get('SKYPE_USERNAME'))
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]'))).click()

        # Introduce password
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@name="passwd"]'))).send_keys(os.environ.get('SKYPE_PASSWORD'))
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]'))).click()

        # Check box to skip another login
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]'))).click()

        # Click on notification and  tutorial pop-ups
        click_popups()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        logging.error("Skype login failed")
        driver.switch_to.window(driver.window_handles[0])
        handle_exception(e)


def click_popups():
    # Click on notification and  tutorial pop-ups
    WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div[3]/button'))).click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/button'))).click()

# Checks if intercom prompted for inactive user to turn to active state
def check_inactive():
    try:
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox"]'))).click()
        WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Set to active"]'))).click()
    except:
        pass

def skype_call():
    try:
        driver.switch_to.window(driver.window_handles[1])
        # Make the call
        logging.info("Calling")
        # Select user
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-text-as-pseudo-element="Carlos Arias"]'))).click()
        # Click call button
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/button'))).click()
        # Do it without video or audio
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[1]/div[3]/div[3]/div/div/div/div[2]/div[2]/div/button'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/button'))).click()
        except:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/button'))).click()
            pass

        # Say hello on intercom
        driver.switch_to.window(driver.window_handles[0])
        say_hello()
        driver.switch_to.window(driver.window_handles[1])

        # Wait for the hang_up
        time.sleep(60)
        logging.info("Ended call")
        driver.refresh()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        driver.refresh()
        logging.error("Call failed")
        driver.switch_to.window(driver.window_handles[0])
        handle_exception(e)

def get_customer_name():
    try:
        # Click on my profile name
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Your inbox"]'))).click()

        # Get the name of the customer name in the list
        customer_item = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="flex flex-row items-center h-4"]')))
        customer_item.click()
        customer_name = customer_item.text.replace('\n', '')
        return customer_name
    except:
        return ''
        pass


def is_expert_chat():
    # Detect if Expert or T2 mention in any message
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div[1]//*[contains(text(), "Expert") or contains(text(), "@T2") or contains(text(), "Tier") or contains(text(), "assist")]')))
        logging.debug("Is an expert chat")
        return True
    except:
        pass
    # Detect if there is a note
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div[1]//*[@data-part-group-category="4"]')))
        logging.debug("Is an expert chat transfered from T1")
        return True
    except:
        logging.debug("NOT an expert chat")
        return False


def say_hello():
    try:
        # Make sure it's in reply mode, not note
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div/a'))).send_keys('r')
        textbox = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//*[@role="textbox"]')))
        textbox.send_keys('#carlos_hello')
        textbox.send_keys(Keys.ENTER)
        time.sleep(1)
        textbox.send_keys(Keys.CONTROL + Keys.ENTER)
        time.sleep(1)
        logging.info("Say Hello to student")
    except:
        logging.error("Failed to say Hello")

# Main
logging.info("Starting selenium script")
intercom_login()
intercom_change_status("Active")
skype_login()
customer_name = ''
new_customer_name = ''
activated = False

while True:
    # Check that there is no inactive dialog
    check_inactive()

    # Get customer's name
    new_customer_name = get_customer_name()

    # If there is no customer online, reset the customer_name variables
    if new_customer_name == '': customer_name = ''

    # If it's an expert chat, and it hasn't called before because of it, make a call
    if is_expert_chat() and customer_name != new_customer_name:
        logging.info("New chat from: " + new_customer_name)
        skype_call()
        customer_name = new_customer_name

    time.sleep(2)

    current_utc_time = datetime.utcnow()

    if current_utc_time.hour >= 14 and current_utc_time.minute == 30:
        logging.info("Ending day")
        intercom_change_status("Away")
        break

# Closing instance to save memory
driver.quit()
