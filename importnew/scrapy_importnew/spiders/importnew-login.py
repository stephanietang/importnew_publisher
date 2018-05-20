# -*- coding:utf-8 -*-
import scrapy
import re
from scrapy.exceptions import CloseSpider

from scrapy_importnew.items import *

class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ['http://www.importnew.com/wp-login.php']

    def parse(self, response):
        print('access login page ' + response.url)
        yield scrapy.FormRequest(
            url='http://www.importnew.com/wp-login.php',
            formdata={
                'log': 'input your username',
                'pwd': 'input your password',
            },
            callback=self.after_login,
        )

    def after_login(self, response):
        print('!!!! access ' + response.url)

        edit_page = 'http://www.importnew.com/wp-admin/edit.php'

        yield response.follow(edit_page, callback=self.parse_edit_page)
        

    def parse_edit_page(self, response):
        print('!!! access '+ response.url)

        for post in response.css('tr.post'):

            title = post.css('td a.row-title::text').extract_first()
            trimmed_title = re.sub(r'\s+', '', title)
            link = post.css('td a.row-title::attr(href)').extract_first()
            link = link.split('?')[1].split('&')[0].split('=')[1]
            link = 'http://www.importnew.com/' + link + '.html'
            date_str =  post.css('td.date abbr::text').extract_first()
            date = int(date_str.replace('-', ''))
            category = post.css('td.categories a::text').extract_first()
            tags = post.css('td.tags a::text').extract()
            view = post.css('td.views::text').extract_first()
            view = view.split(' ')[0]
            view = int(view.replace(',', ''))

            item = ScrapyImportnewItem()
            item['title'] = trimmed_title
            item['link'] = link
            item['date'] = date
            item['view'] = view
            item['tags'] = tags
            item['category'] = category
            if view > 10:
                yield item
        
        next_page = response.css('a.next-page::attr(href)').extract_first()
        pageNum = next_page.split('=')[1]
        
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_edit_page,
            )
            
