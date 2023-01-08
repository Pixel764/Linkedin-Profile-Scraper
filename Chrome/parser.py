import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_username(browser: webdriver.Chrome):
    try:
        return browser.find_element(By.CSS_SELECTOR, 'h1[class="text-heading-xlarge inline t-24 v-align-middle break-words"]').text
    except NoSuchElementException:
        return 'None'


def get_description(browser: webdriver.Chrome):
    try:
        return browser.find_element(By.CSS_SELECTOR, 'div[class="text-body-medium break-words"').text
    except NoSuchElementException:
        return 'None'


def get_location(browser: webdriver.Chrome):
    try:
        return browser.find_element(By.CSS_SELECTOR, 'span[class="text-body-small inline t-black--light break-words"]').text
    except NoSuchElementException:
        return 'None'


def get_followers(browser: webdriver.Chrome):
    try:
        return browser.find_element(By.CSS_SELECTOR, 'ul[class="pv-top-card--list pv-top-card--list-bullet"]').find_element(By.CSS_SELECTOR, 'li[class="text-body-small t-black--light inline-block"]').find_element(By.TAG_NAME, 'span').text
    except NoSuchElementException:
        return 'None'


def get_profile_image_url(browser: webdriver.Chrome):
    try:
        img_url = browser.find_element(By.CSS_SELECTOR, 'div[class="pv-top-card__non-self-photo-wrapper ml0"]').find_element(By.TAG_NAME, 'img').get_attribute('src')
        if img_url == 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7':
            return 'Default'
        return img_url
    except NoSuchElementException:
        return 'None'


def get_join_in(browser: webdriver):
    try:
        action = ActionChains(browser)

        button_more = browser.find_element(By.CSS_SELECTOR, 'div[class="pv-top-card-v2-ctas"]').find_element(By.CSS_SELECTOR, 'button[aria-label="More actions"]')
        button_about_this_profile = browser.find_element(By.CSS_SELECTOR, 'div[class="pv-top-card-v2-ctas"]').find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')[-1].find_element(By.CSS_SELECTOR, 'div[role="button"]')

        action.click(button_more).perform()
        time.sleep(1)
        action.click(button_about_this_profile).perform()
        join_in = browser.find_element(By.CSS_SELECTOR, 'ul[class="list-style-none pt1"]').find_element(By.CSS_SELECTOR, 'span[class="tvm__text tvm__text--neutral"]').text
        return join_in
    except NoSuchElementException:
        return 'None'


info_functions = {
    'Username': get_username,
    'Join in': get_join_in,
    'Followers': get_followers,
    'Description': get_description,
    'Location': get_location,
    'ImageURL': get_profile_image_url
}


def get_line(browser: webdriver.Chrome) -> str:
    line = []  # Line what will be added in file
    for func in info_functions.values():
        line.append(func(browser))
    return ','.join(line) + '\n'


def parse_profiles(profile_urls: list, cookies, time_per_page: int) -> None:
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')

    print('Parsing has start...')
    with webdriver.Chrome(service=service, options=options) as browser:
        browser.get('https://www.linkedin.com/home')
        browser.implicitly_wait(4)

        for cookie in cookies:
            browser.add_cookie(cookie)

        url_numb = 1
        with open('result.csv', 'w', encoding='utf-8') as result_file:
            titles = []
            for title in info_functions.keys():
                titles.append(title)

            result_file.write(','.join(titles) + '\n')

            for url in profile_urls:
                try:
                    browser.get(url)
                    time.sleep(time_per_page)  # User imitation
                    result_file.write(get_line(browser))
                except Exception as ex:
                    print(
                        f'[{url_numb}]...[❌] \n'
                        '-------------------- \n'
                        f'{ex}'
                    )
                    break
                else:
                    print(f'[{url_numb}]...[✔️]')
                    url_numb += 1
        print('Finish!')
