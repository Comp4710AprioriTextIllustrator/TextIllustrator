import datacollecter
import scrapy
import re

class BbcSpider(scrapy.Spider):
    # Name must be specified outside of the constructor in order to be able to crawl using this spider
    name = "bbc"
    max_articles = 2000
    
    def __init__(self, *args):
        self.allowed_domains = ["bbc.com", "bbc.co.uk"]
        self.start_urls = ["http://www.bbc.com"]
        self.news_re = re.compile('.*\/news\/.*')
        # Ignore specific links
        self.invalid_res = [
            re.compile('.*comments.*'),
            re.compile('.*\/live\/.*'),
            re.compile('.*\/blogs\/.*')
        ]
        self.supported_news_domains = {
            self.news_re: self.parse_world_article
        }
        
        self.articles_seen = []
        self.article_count = 0
    
        scrapy.Spider.__init__(self, *args)
    
    def parse(self, response):
        articles_on_page = response.xpath("//a//@href")
        for article_url in articles_on_page:
            if self.news_re.match(article_url.extract()):
                full_article_url = response.urljoin(article_url.extract())
                yield scrapy.Request(full_article_url, callback=self.parse_article)
    
    def parse_article(self, response):
        # Only works for specific sections
        if response.url not in self.articles_seen and self.crawler.stats.get_value('pages_crawled') < self.max_articles:
            for supported_news_domain in self.supported_news_domains:
                if supported_news_domain.match(response.url):
                    article_item = self.supported_news_domains[supported_news_domain](response)
                    if article_item and response.url not in self.articles_seen:
                        self.crawler.stats.inc_value('pages_crawled')
                        yield article_item
        
            articles_on_page = response.xpath("//a//@href")
            for article_url in articles_on_page:
                if self.news_re.match(article_url.extract()):
                    invalid = False
                    for invalid_re in self.invalid_res:
                        if invalid_re.match(article_url.extract()):
                            invalid = True
                            break
                            
                    if invalid or article_url.extract() in self.articles_seen:
                        continue
                            
                    if self.crawler.stats.get_value('pages_crawled') < self.max_articles:
                        self.articles_seen.append(response.url)
                        full_article_url = response.urljoin(article_url.extract())
                        yield scrapy.Request(full_article_url, callback=self.parse_article)
        
    def parse_world_article(self, response):
        title = response.xpath("//h1[@class = 'story-body__h1']//text()[1]").extract()
        text = response.xpath("//div[@class ='story-body']//p//text()").extract()
        
        # Ensure there is a title for the articles
        if len(title) == 0:
            return None
        
        article_item = datacollecter.items.ArticleItem()
        article_item['title'] = title[0]
        article_item['text'] = text
        article_item['url'] = response.url
        return article_item
        