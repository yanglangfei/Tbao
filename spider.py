import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
from pyquery import PyQuery as pq
import pymongo
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
option = webdriver.ChromeOptions()
# option.add_argument("headless")
# option.add_argument('--proxy-server=127.0.0.1:8080')
browser = webdriver.Chrome(options=option)
wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        input.send_keys(KEY_WORD)
        submit.click()
        time.sleep(15)
        total = wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        # main_driver = browser.current_window_handle
        js = "window.scrollTo(0,document.body.scrollHeight)"
        browser.execute_script(js)
        get_product()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        print('next page:', page_num)
        page_input = wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        page_btn = wait.until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        page_input.clear()
        page_input.send_keys(page_num)
        page_btn.click()
        wait.until(
            ec.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_num))
        )
        time.sleep(5)
        js = "window.scrollTo(0,document.body.scrollHeight)"
        browser.execute_script(js)
        get_product()
    except TimeoutException:
        next_page(page_num)


def save_to_mongo(result):
    try:
        if db[MONGO_DB].insert(result):
            print('save success', result)
    except Exception:
        print('save error', result)


def get_product():
    wait.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        browser.implicitly_wait(10)
        save_to_mongo(product)


def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total + 1):
            next_page(i)
    except Exception:
        print('main error')
    finally:
        browser.close()


if __name__ == '__main__':
    main()
