import datacollecter
import scrapy

class NyTimesSpider(scrapy.Spider):
    name = "nytimes"
    allowed_domains = ["nytimes.com"]
    start_urls = ["http://www.nytimes.com"]
    
    def parse(self, response):
        # Get the top news story links
        articles_on_page = response.xpath("//h1[@class = 'story-heading']//a[1]//@href")
        # Get all other story links
        articles_on_page.extend(response.xpath("//h2[@class = 'story-heading']//a[1]//@href"))
        
        for article in articles_on_page:
            full_article_url = response.urljoin(article.extract())
            yield scrapy.Request(full_article_url, callback=self.parse_article)
        
    def parse_article(self, response):
        # Only want the h1 story-headings, so story links on the page are not accidentally pulled as well
        utf8_title = ' '.join(response.xpath("//h1[@id = 'story-heading']//text()").extract())
        title = self.__remove_non_ascii_chars(utf8_title)
        
        # Ignore articles with no title, a few links to non-article pages are being returned and I'm not sure why
        if len(title) >= 1:
            utf8_text = '\n'.join(response.xpath("//article[@id = 'story']//p[@class = 'story-body-text story-content']//text()").extract())
            text = self.__remove_non_ascii_chars(utf8_text)
            
            article_item = datacollecter.items.ArticleItem()
            article_item['title'] = title
            article_item['text'] = text
            yield article_item

    def __remove_non_ascii_chars(self, utf8_text):
        utf8_char_string = []
        utf8_char_string.extend(utf8_text)
        return ''.join([char for char in utf8_char_string if ord(char) < 128])