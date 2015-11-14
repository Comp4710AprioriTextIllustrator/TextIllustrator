import scrapy
#from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from datacollecter.items import ArticleItem

class volkskrantnlSpider(scrapy.Spider):
    name = "volkskrant"
    allowed_domains = ["volkskrant.nl"]
    start_urls = ["http://www.volkskrant.nl"]
    count = 0
    max_count = 100000

    def parse(self, response):
        articles_onpage = response.xpath('.//@href')
        #if self.is_article(response):
        #yield self.parse_article(response)

        #yield scrapy.Request(response.url, callback=self.parse_article)
        print response.url
        item = ArticleItem()
        article = response.xpath('//article[re:test(@class, "article article--full")]') #including images, but not ads (preferably)
        time = article.xpath('.//time[re:test(@class, "article__meta-time")]/text()').extract()
        title = article.xpath('.//h1[re:test(@class, "article__title")]/text()').extract()
        intro = article.xpath('.//p[re:test(@class, "article__intro")]/text()').extract()
        #body = article.xpath('.//p[re:test(@class, "article__body__paragraph")]/text()').extract()
        all_text = article.xpath('.//text()').extract()
        if len(title) >= 1 and len(intro) >= 1 and len(all_text) >= 1:
            item['title'] = title
            item['time'] = time
            item['text'] = all_text
            item['url'] = response.url
            self.count = self.count + 1
            print self.count
            yield item

        if self.count < self.max_count:
            for article in articles_onpage:
                url = article.extract()
                for ad in self.allowed_domains:
                    if url.startswith(ad) or url.startswith("http://www." + ad):
                        yield scrapy.Request(url, callback=self.parse)
                    elif url.startswith("/cookiewall/accept?"):
                        yield scrapy.Request(self.start_urls[0] + url, callback=self.parse)
                    elif url.startswith("/"):
                        urln = "http://" + ad + url
                        yield scrapy.Request(urln, callback=self.parse)
        else:
            print "MAX ARTICLE COUNT EXCEEDED"

    def parse_article(self, response):
        """parse article for text and images"""
        #print response.url
        #print "URL: " + response.url
        item = ArticleItem()
        article = response.xpath('//article[re:test(@class, "article article--full")]') #including images, but not ads (preferably)
        time = article.xpath('.//time[re:test(@class, "article__meta-time")]/text()').extract()
        title = article.xpath('.//h1[re:test(@class, "article__title")]/text()').extract()
        intro = article.xpath('.//p[re:test(@class, "article__intro")]/text()').extract()
        #body = article.xpath('.//p[re:test(@class, "article__body__paragraph")]/text()').extract()
        all_text = article.xpath('.//text()').extract()
        if len(title) >= 1 and len(intro) >= 1 and len(all_text) >= 1:
            item['title'] = title
            item['time'] = time
            item['text'] = all_text
            item['url'] = response.url
            self.count = self.count + 1
            print item
            print "COUNT: ", self.count
            yield item
        #content = response.xpath('.//[re:test(@id, "page-main-content")]//div[re:test@class, "col--primary"])')
