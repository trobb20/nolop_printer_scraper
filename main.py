import requests
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

def setup_driver():
    cd = pathlib.Path('./chrome/chromedriver')
    driver = webdriver.Chrome(cd)
    return driver

def open_page(driver, p_num):
    URL = "https://p"+str(p_num)+".nolop.org/?#temp"
    driver.get(URL)
    return

def login(driver, user, pwd):
    user_box = driver.find_element(By.ID, "login-user")
    pass_box = driver.find_element(By.ID, 'login-password')
    login_button = driver.find_element(By.ID, 'login-button')
    user_box.send_keys(user)
    pass_box.send_keys(pwd)
    login_button.click()

def get_print_time_from_printer(driver, p_num):
    # we're in

    info_box = driver.find_element(By.CLASS_NAME, "accordion-inner")
    print(info_box.text) ## fix this!!

def is_page_loaded(driver, timeout):
    count = 0
    try:
        loading_container = driver.find_element(By.ID, "page-container-loading")
    except:
        sleep(1)
        count = count + 1
        if count > timeout:
            print("Could not load webpage")
            raise
    else:
        while loading_container.text != '':
            sleep(1)
            count = count + 1
            if count > timeout:
                print("Could not load webpage")
                raise
        return True

def get_state_info():
    state_string = driver.find_element(By.ID, 'state').text
    state_list = [i.split(':') for i in state_string.split('\n')]
    print(state_list)

driver = setup_driver()
open_page(driver, 3)
login(driver, 'nolop', '3dprint')
while not is_page_loaded(driver, 15):
    pass
print('Page loaded.')
for i in range(15):
    get_state_info()
    sleep(1)
driver.quit()