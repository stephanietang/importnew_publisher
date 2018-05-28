# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import json
import account

username=account.login
password=account.password

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
driver.get('https://mp.weixin.qq.com/')
time.sleep(2)
driver.find_element_by_xpath("./*//input[@name='account']").clear()
driver.find_element_by_xpath("./*//input[@name='account']").send_keys(username)
driver.find_element_by_xpath("./*//input[@name='password']").clear()
driver.find_element_by_xpath("./*//input[@name='password']").send_keys(password)

time.sleep(5)
driver.find_element_by_xpath("./*//a[@class='btn_login']").click()
# scan qr code using phone
time.sleep(15)
driver.get('https://mp.weixin.qq.com/')
cookie_items = driver.get_cookies()

post = {}
for cookie_item in cookie_items:
    post[cookie_item['name']] = cookie_item['value']
cookie_str = json.dumps(post)
with open('cookie.txt', 'w+', encoding='utf-8') as f:
    f.write(cookie_str)
