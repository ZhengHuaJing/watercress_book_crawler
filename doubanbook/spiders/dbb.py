# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from doubanbook.items import DoubanbookItem
from scrapy.http import Request, FormRequest, HtmlResponse


class DbbSpider(CrawlSpider):
    name = 'dbb'
    allowed_domains = ['book.douban.com']
    start_urls = []

    # 取出所有标签名
    url = 'https://book.douban.com/tag/'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'}
    response = requests.get(url = url, headers = headers).text
    tag_names = etree.HTML(response).xpath('//table[@class="tagCol"]//a/text()')

    # 将所有url添加进start_urls列表
    for tag_name in tag_names:
        start_urls.append(url + tag_name)

    rules = (
        Rule(LinkExtractor(allow = r'/tag/.+\?start=\d+&type=T'), callback = 'parse_item', follow = True),
    )   

    # 构造请求头
    post_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://accounts.douban.com/login?source=book',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded'
    }   

    def start_requests(self):
        """
            请求登录界面
        """
        return [
            Request(
                url = 'https://accounts.douban.com/login?source=book', 
                meta = {'cookiejar': 1},
                callback = self.post_login
            )
        ]

    def post_login(self, response):
        """
            发送post请求模拟登陆
        """
        formdata = {
            'source': 'book',
            'redir': 'https%3A%2F%2Fbook.douban.com%2Ftag%2F%3Fview%3Dtype%26icn%3Dindex-sorttags-all',
            'form_email': 'username',
            'form_password': 'password',
            'login': '%E7%99%BB%E5%BD%95'
        }
        # 获取隐藏表单参数captcha-id
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract()
        if captcha_id:
            formdata['captcha-id'] = captcha_id[0]
        # 输入验证码
        captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract()
        if captcha_image_url:
            with open('captcha_image.jpg', 'wb') as file:
                file.write(requests.get(captcha_image_url[0]).content)
            captcha_solution = raw_input('请输入验证码')
            formdata['captcha-solution'] = captcha_solution

        return [
            FormRequest.from_response(
                response,
                url = 'https://accounts.douban.com/login',
                meta = {'cookiejar': response.meta['cookiejar']},
                headers = self.post_headers,
                formdata = formdata,
                callback = self.after_login,
                dont_filter = True
            )
        ]

    def after_login(self, response):
        """
            将start_urls中的每个请求增加cookie参数
        """
        for url in self.start_urls:
            yield Request(url, meta = {'cookiejar': response.meta['cookiejar']})

    def _requests_to_follow(self, response):  
        """
            重写加入cookiejar的更新
        """  
        if not isinstance(response, HtmlResponse):  
            return  
        seen = set()  
        for n, rule in enumerate(self._rules):  
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]  
            if links and rule.process_links:  
                links = rule.process_links(links)  
            for link in links:  
                seen.add(link)  
                r = Request(url=link.url, callback=self._response_downloaded)  
                # 下面这句是我重写的  
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])  
                yield rule.process_request(r)

    def get_item_count(self, response):
        """
            返回item的个数
        """
        return len(response.xpath('//li[@class="subject-item"]').extract())

    def get_book_name(self, response, index):
        """
            返回书名
        """
        book_name = response.xpath('//li[@class="subject-item"][' + str(index) + ']/div[@class="info"]/h2/a/@title').extract()

        if book_name:
            book_name = '《' + book_name[0].encode('utf-8') + '》'
        else:
            book_name = 'NULL'

        return book_name

    def get_info(self, response, index):
        """
            返回出版信息
        """
        info = response.xpath('//li[@class="subject-item"][' + str(index) + ']/div[@class="info"]/div[@class="pub"]/text()').extract()

        if info:
            info = info[0].strip()
        else:
            info = response.xpath('//div[@class="sc-bZQynM cOULRN sc-bxivhb eHmSYu"][' + str(index) + ']//div[@class="meta abstract"]/text()').extract()
            if info:
                info = info[0].strip()
            else:
                info = 'NULL'

        return info

    def get_intro(self, response, index):
        """
            返回简介
        """
        intro = response.xpath('//li[@class="subject-item"][' + str(index) + ']/div[@class="info"]/p/text()').extract()

        if intro:
            intro = intro[0]
        else:
            intro = 'NULL'

        return intro

    def get_grade(self, response, index):
        """
            返回评分
        """
        grade = response.xpath('//li[@class="subject-item"][' + str(index) + ']/div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract()

        if grade:
            grade = grade[0]
        else:
            grade = 'NULL'

        return grade

    def get_evaluate_number(self, response, index):
        """
            返回评价人数
        """
        evaluate_number = response.xpath('//li[@class="subject-item"][' + str(index) + ']/div[@class="info"]/div[@class="star clearfix"]/span[@class="pl"]/text()').extract()

        if evaluate_number:
            evaluate_number = evaluate_number[0].encode('utf-8').replace('(', '').replace(')', '').strip()
        else:
            evaluate_number = 'NULL'

        return evaluate_number

    def get_source_url(self, response, index):
        """
            返回来源链接
        """
        source_url = response.xpath('//li[@class="subject-item"][' + str(index) + ']/div[@class="pic"]/a/@href').extract()

        if source_url:
            source_url = source_url[0]
        else:
            source_url = 'NULL'

        return source_url


    def parse_item(self, response):
        """
            解析页面数据
        """
        # 根据页面中item的总数，遍历解析出每个item
        for i in range(self.get_item_count(response)):
            item = DoubanbookItem()

            # 书名
            item['book_name'] = self.get_book_name(response, i)
            # 出版信息
            item['info'] = self.get_info(response, i)
            # 简介
            item['intro'] = self.get_intro(response, i)
            # 评分
            item['grade'] = self.get_grade(response, i)
            # 评价人数
            item['evaluate_number'] = self.get_evaluate_number(response, i)
            # 来源链接
            item['source_url'] = self.get_source_url(response, i)
            # 来源名称
            item['source_name'] = 'douban'

            yield item






















