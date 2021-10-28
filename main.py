import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def setup_driver(driver_path) -> webdriver:
    """
    Sets up the selenium web driver, given a path to the chrome
    driver. Returns webdriver object
    :param driver_path: path to chrome driver (including chrome driver in path)
    :return: webdriver object
    """
    cd = pathlib.Path(driver_path)
    driver = webdriver.Chrome(cd)
    return driver


def open_page(driver, p_num) -> None:
    """
    Opens a printer's webpage
    :param driver: webdriver to open with
    :param p_num: printer number
    :return: None
    """
    URL = "https://p" + str(p_num) + ".nolop.org/?#temp"
    driver.get(URL)
    return


def login(driver, user, pwd) -> None:
    """
    Logs into octoprint
    :param driver: webdriver
    :param user: username
    :param pwd: password
    :return: None
    """
    user_box = driver.find_element(By.ID, "login-user")
    pass_box = driver.find_element(By.ID, 'login-password')
    login_button = driver.find_element(By.ID, 'login-button')
    user_box.send_keys(user)
    pass_box.send_keys(pwd)
    login_button.click()
    return


def is_page_loaded(driver, timeout) -> bool:
    """
    Waits until the printer's octoprint page has loaded
    enough to get significant data, by checking different aspects
    of webpage
    :param driver: webdriver
    :param timeout: seconds to wait before raising an error
    :return: True when loaded
    """
    count = 0
    # Wait until loading page is gone
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
    # Wait until states load into the page
    state_status = ''
    while state_status == '':
        try:
            state_status = get_state_info()['State']
        except KeyError:
            pass
        sleep(1)
        count = count + 1
        if count > timeout:
            print("Could not load webpage")
            raise
    return True


def get_state_info(driver) -> dict:
    """
    Gets the state info from a printer's webpage. This can include:
    State, Resend ratio, File, Uploaded, User, Print time, Print time remaining, Printed data
    :param driver: webdriver
    :return: dict of the states and their values
    """
    state_string = driver.find_element(By.ID, 'state').text
    state_list = [i.split(':') for i in state_string.split('\n')]
    state_dict = {}
    for state in state_list:
        state_name = state[0]
        state_contents = ''
        for i in state[1:]:
            state_contents = state_contents + i
        state_dict[state_name] = state_contents
    return state_dict


def get_time_remaining_on_print(state) -> str:
    """
    Returns the print time remaining in plaintext as is appears on the webpage
    :param state:
    :return:
    """
    s = state['Print Time Left']
    return s[0:-1]


def main():
    driver = setup_driver()
    for i in range(8):
        p = i + 1
        print('Checking p%s' % p)
        open_page(driver, p)
        print('Logging in...')
        login(driver, 'nolop', '3dprint')
        while not is_page_loaded(driver, 15):
            pass
        print('Loaded page.')
        state = get_state_info()
        print('Print time remaining is: ' + get_time_remaining_on_print(state))
    driver.quit()


if __name__ == 'main':
    main()
