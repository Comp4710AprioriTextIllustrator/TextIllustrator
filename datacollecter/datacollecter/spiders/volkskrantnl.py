import scrapy
from crawler.items import ArticleItem

class volkskrantnlSpider:
    name = "volkskrant"
    allowed_domains = ["volkskrant.nl"]
    start_urls = ["http://www.volkskrant.nl"]

    def parse(self, response):
        """find articles"""
        articles_onpage = response.xpath('.//[re:test(@class, "ankeiler")//@href')
        for article in articles_onpage:
            url = article
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        """parse article for text and images"""
        content = response.xpath('.//[re:test(@id, "page-main-content")]//div[re:test@class, "col--primary"])')

