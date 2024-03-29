import time

from selenium import webdriver
from config import *

# 爬取 QQ 空间说说
driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.maximize_window()


def load_qq_page(qq):
    driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
    time.sleep(3)
    try:
        driver.find_element_by_id('login_div')
        # 是否需要登录
        a = True
    except:
        a = False
    if a == True:
        login(ACCOUNT, PASSWORD)
        time.sleep(3)
    driver.implicitly_wait(3)
    try:
        # 是否可以访问
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False
    if b == True:
        driver.switch_to.frame('app_canvas_frame')
        driver.implicitly_wait(5)
        js = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
        driver.implicitly_wait(3)
        driver.save_screenshot('./qq.png')
        content = driver.find_elements_by_css_selector('.content')
        stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        header = driver.find_element_by_css_selector(
            '#msgList > li:nth-child(1) > div.avatar > a > img')
        nickname = driver.find_element_by_css_selector('#msgList > li:nth-child(3) > div.box.bgr3 > div.bd > a')
        for con, sti in zip(content, stime):
            data = {
                'header': header.get_attribute('src'),
                'nickname': nickname.text,
                'time': sti.text,
                'shuo': con.text
            }
            print(data)
    cookie = driver.get_cookies()
    cookie_dict = []
    for c in cookie:
        ck = "{0}={1};".format(c['name'], c['value'])
        cookie_dict.append(ck)
    i = ''
    for c in cookie_dict:
        i += c
    print('Cookies:', i)
    print("==========完成================")


def login(account, password):
    driver.switch_to.frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_id('u').clear()  # 选择用户名框
    driver.find_element_by_id('u').send_keys(account)
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('p').send_keys(password)
    driver.find_element_by_id('login_button').click()


def main():
    qq = input('请输入爬取的QQ:')
    load_qq_page(qq)
    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
