import scrapy
import re

class BbcSpider(scrapy.Spider):
    name = "bbc"
    
    def __init__(self, *args):
        self.allowed_domains = ["bbc.com"]
        self.start_urls = ["http://www.bbc.com"]
        self.supported_news_domains = {
            re.compile('.*news\/world-.*'): self.parse_world_article
        }
    
        scrapy.Spider.__init__(self, *args)
    
    def parse(self, response):
        articles_on_page = response.xpath("//a[@class = 'block-link__overlay-link']//@href")
        for article_url in articles_on_page:
            full_article_url = response.urljoin(article_url.extract())
            yield scrapy.Request(full_article_url, callback=self.parse_article)
    
    def parse_article(self, response):
        # Only works for specific sections
        for supported_news_domain in self.supported_news_domains:
            if supported_news_domain.match(response.url):
                self.supported_news_domains[supported_news_domain](response)
        
    def parse_world_article(self, response):
        title = response.xpath("//h1[@class = 'story-body__h1']//text()[1]").extract()
        if len(title) >= 1:
            print "TITLE = %s" % (title[0])