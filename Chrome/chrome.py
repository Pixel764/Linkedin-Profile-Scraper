import pickle
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from Chrome.parser import parse_profiles
import os


def login() -> None:
    print('Login...')
    with webdriver.Chrome() as browser:
        browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        time.sleep(1)

        # Take fields
        try:
            username_field = browser.find_element(By.ID, 'username')
            password_field = browser.find_element(By.ID, 'password')
        except NoSuchElementException:
            print('Not Found login fields!')
            exit()

        # Delete the data from the field
        username_field.clear()
        password_field.clear()

        # Set data in fields
        username_field.send_keys(os.getenv('ACCOUNT_LOGIN'))
        time.sleep(1)
        password_field.send_keys(os.getenv('ACCOUNT_PASSWORD'))
        time.sleep(1)

        # Send form
        password_field.send_keys(Keys.ENTER)

        # Check if username or email is correct
        try:
            browser.find_element(By.ID, 'error-for-username')
        except NoSuchElementException:
            print('Incorrect username or email!')
            exit()

        # Check if password is correct
        try:
            browser.find_element(By.ID, 'error-for-password')
        except NoSuchElementException:
            print('Incorrect Password!')
            exit()
        # Save cookies in file
        pickle.dump(browser.get_cookies(), open('cookies', 'wb'))


def get_cookies():
    try:
        with open('cookies', 'rb') as cookie_file:
            cookies = pickle.load(cookie_file)
    except FileNotFoundError:
        login()
        get_cookies()
    else:
        return cookies


def check_cookies(test_url: str):
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')
    cookies = get_cookies()

    try:
        # Check if cookies is old
        print('Checking cookies...')
        with webdriver.Chrome(service=service, options=options) as browser:
            browser.get('https://www.linkedin.com/home')

            for cookie in cookies:
                browser.add_cookie(cookie)

            browser.get(test_url)
            browser.implicitly_wait(4)
            browser.find_element(By.CSS_SELECTOR, 'h1[class="text-heading-xlarge inline t-24 v-align-middle break-words"]')  # Try to find username
    except NoSuchElementException:
        login()
    except Exception as ex:
        print(ex)
        exit()
    finally:
        print(f'Cookies status: [✔️]')
        return get_cookies()


def start(profile_urls: list, time_per_page):
    cookies = check_cookies(profile_urls[0])
    parse_profiles(profile_urls, cookies, time_per_page)
