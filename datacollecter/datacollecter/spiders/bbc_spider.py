import datacollecter
import scrapy
import re

class BbcSpider(scrapy.Spider):
    # Name must be specified outside of the constructor in order to be able to crawl using this spider
    name = "bbc"
    
    def __init__(self, *args):
        self.allowed_domains = ["bbc.com", "bbc.co.uk"]
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
                article_item = self.supported_news_domains[supported_news_domain](response)
                if article_item:
                    yield article_item
        
    def parse_world_article(self, response):
        title = response.xpath("//h1[@class = 'story-body__h1']//text()[1]").extract()
        text = response.xpath("//div[@class ='story-body']//p//text()").extract()
        
        # Ensure there is a title for the articles
        if len(title) == 0:
            return None
        
        article_item = datacollecter.items.ArticleItem()
        article_item['title'] = title[0]
        article_item['text'] = text
        return article_item
        