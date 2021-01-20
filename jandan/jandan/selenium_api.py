from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def setup_driver(browser, driver_path):
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--user-data-dir=C:/Users/shaohua/AppData/Local/Google/Chrome/User Data/Profile 1")

    if browser == 'chrome':
        driver = webdriver.Chrome(driver_path, options=options)
        return driver
    else:
        # for firefox...
        pass


default_time_out = 10
default_message = '-'


def wait_for_alert_is_present(driver, message=default_message, timeout=default_time_out):
    WebDriverWait(driver, timeout).until(EC.alert_is_present(), message)


def wait_for_element_present(driver, locator, message=default_message, timeout=default_time_out):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator), message)
    return element


def wait_for_elements_present(driver, locator, message=default_message, timeout=default_time_out):
    elements = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator), message)
    return elements


def wait_for_text_to_be_present_in_element(driver, locator, text,
                                           message=default_message, timeout=default_time_out):
    # <p>this is text</p>
    element = WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element(locator, text), message)
    return element


def wait_for_text_to_be_present_in_element_value(driver, locator, text,
                                                 message=default_message, timeout=default_time_out):
    # <input type="text" value="text value">
    element = WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element_value(locator, text), message)
    return element


def send_keys_to_element(driver, locator, keys, message=default_message, timeout=default_time_out):
    wait_for_element_present(driver, locator, message, timeout).send_keys(keys)
    wait_for_text_to_be_present_in_element_value(driver, locator, keys, message, timeout)


def wait_for_url_to_be(driver, url, message=default_message, timeout=default_time_out):
    WebDriverWait(driver, timeout).until(EC.url_to_be(url), message)


def wait_for_url_contains(driver, url, message=default_message, timeout=default_time_out):
    WebDriverWait(driver, timeout).until(EC.url_contains(url), message)


def navigate_to(driver, url, message=default_message, timeout=default_time_out):
    driver.get(url)
    wait_for_url_contains(driver, url, message, timeout)


def wait_for_element_to_be_clickable(driver, locator, message=default_message, timeout=default_time_out):
    # visible and enabled
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator), message)


def wait_for_element_absent(driver, locator, message=default_message, timeout=default_time_out):
    # element is either a locator (text) or an WebElement
    return WebDriverWait(driver, timeout).until(EC.invisibility_of_element(locator), message)


def scroll_to_element(driver, element):
    driver.execute_script("return arguments[0].scrollIntoView();", element)
    driver.execute_script("window.scrollBy(0, -100);")


def scroll_to_locator(driver, locator, message=default_message, timeout=default_time_out):
    element = wait_for_element_present(driver, locator, message, timeout)
    scroll_to_element(driver, element)


def click_button(driver, locator, message=default_message, timeout=default_time_out):
    return wait_for_element_to_be_clickable(driver, locator, message, timeout).click()


def scroll_to_and_click_button(driver, locator, message=default_message, timeout=default_time_out):
    scroll_to_locator(driver, locator, message, timeout)
    return click_button(driver, locator, message, timeout)


def select_text_from_drop_down(driver, locator, text, message=default_message, timeout=default_time_out):
    drop_down_list = Select(wait_for_element_present(driver, locator, message, timeout))
    wait_for_drop_down_list_to_be_populated(driver, drop_down_list)
    drop_down_list.select_by_visible_text(text)


def select_value_from_drop_down(driver, locator, value, message=default_message, timeout=default_time_out):
    drop_down_list = Select(wait_for_element_present(driver, locator, message, timeout))
    wait_for_drop_down_list_to_be_populated(driver, drop_down_list)
    drop_down_list.select_by_value(value)


def wait_for_drop_down_list_to_be_populated(driver, selector, timeout=default_time_out):
    waited_time = 0
    while waited_time < timeout:
        if len(selector.options) > 0:
            break
        waited_time += 0.5
        driver.implicitly_wait(0.5)


def wait_for_new_window_to_be_open(driver, message=default_message, timeout=default_time_out):
    WebDriverWait(driver, timeout).until(EC.new_window_is_opened(driver.window_handles), message)
