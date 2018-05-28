importnew crawler
========================

This project uses [Scrapy](https://scrapy.org/) to crawl the posts in [importnew](www.importnew.com)

Before crawling the posts, you have to 

- install python
- install Scrapy
- install mongodb(by default mongodb would be installed on localhost:27017)
- you must have login account of importnew

How to crawl the posts from importnew
---------------

1. The username/password is set up in 

```
<project_root_folder>/importnew/scrapy_importnew/spiders/account.py
```

2. After setting up the accounts, run the command

```
cd <project_root_folder>/importnew/
scrapy crawl login
```

3. After crawling, you will be able to see the posts in mongodb（database="importnewDb", collection="importnewPosts"）