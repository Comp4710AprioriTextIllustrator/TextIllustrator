import scrapy

from datacollecter.items import ArticleItem

class telegraafSpider(scrapy.Spider):
    name = "telegraaf"
    allowed_domains = ["telegraaf.nl", "tmgonlinemedia.nl"]
    start_urls = ["http://www.telegraaf.nl"]

    count = 0
    max_count = 100000

    def parse(self, response):
        articles_onpage = response.xpath('.//@href')
        #if self.is_article(response):
        #yield self.parse_article(response)

        #yield scrapy.Request(response.url, callback=self.parse_article)

        item = ArticleItem()
        article = response.xpath('//div[re:test(@id, "artikel")]') #including images, but not ads (preferably)
        time = article.xpath('.//div[re:test(@class, "artDatePostings")]/span[re:test(@class, "datum")]/text()').extract()
        title = article.xpath('.//h1/text()').extract()
        intro = article.xpath('.//p[re:test(@class, "article__intro")]/text()').extract()
        body = article.xpath('.//div[re:test(@id, "artikelKolom")]//p/text()').extract()
        all_text = article.xpath('.//text()').extract()
        if len(title) >= 1 and len(intro) >= 1 and len(all_text) >= 1:
            item['title'] = title
            item['time'] = time
            item['text'] = ''.join(intro) + ''.join(body) #all_text
            item['url'] = response.url
            self.count = self.count + 1
            print self.count
            print item
            yield item

        if self.count < self.max_count:
            for article in articles_onpage:
                url = article.extract()
                print url
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

