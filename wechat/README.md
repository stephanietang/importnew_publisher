wechat official accounts platform crawler
========================

This project uses python to crawl posts in wechat official accounts platform.

Before crawling, you have to 

- install python
- installl mongodb
- install selenium webdriver(recommend to use chrome as the default browser)
- you must have the imporntew admin account of wechat official accounts platform

How to crawl the posts from wechat official accounts
---------------

1. After installation of nessasary packages, you have to set up your account, the account information is configured in wechat/login_wechat.py

2. After setting up the account information, run the command

```python login_wechat.py```

during the login step, you need to use your mobile phone to scan the QR code. After login successfully, you can see a cookie.txt in this project which can be used for the consequential steps later

3. Execute command to scrawl

```python scrape_wechat.py```

after this step you will be able to see the posts are crawlered in your mongodb