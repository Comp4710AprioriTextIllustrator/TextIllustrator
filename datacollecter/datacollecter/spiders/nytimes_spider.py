import datacollecter
import scrapy
import re

class NyTimesSpider(scrapy.Spider):
    name = "nytimes"
    allowed_domains = ["nytimes.com"]
    start_urls = ["http://www.nytimes.com"]
    max_articles = 2000
    invalid_res = [
        re.compile('.*\/travel\/.*'),
    ]

    def parse(self, response):
        # Get the top news story links
        article_item = self.parse_article(response)
        if article_item is not None and self.crawler.stats.get_value('pages_crawled') < self.max_articles:
            self.crawler.stats.inc_value('pages_crawled')
            yield article_item

        articles_on_page = response.xpath("//a//@href")
        for article in articles_on_page:
            if self.crawler.stats.get_value('pages_crawled') < self.max_articles:
                full_article_url = response.urljoin(article.extract())

                invalid = False
                for invalid_re in self.invalid_res:
                    if invalid_re.match(full_article_url):
                        invalid = True
                        break

                if invalid:
                    yield scrapy.Request(full_article_url, callback=self.parse)

    def parse_article(self, response):
        # Only want the h1 story-headings, so story links on the page are not accidentally pulled as well
        utf8_title = ' '.join(response.xpath("//h1[@id = 'story-heading']//text()").extract())
        title = self.__remove_non_ascii_chars(utf8_title)

        if title is None:
            return None

        # Ignore articles with no title, a few links to non-article pages are being returned and I'm not sure why
        if len(title) >= 1:
            utf8_text = '\n'.join(response.xpath("//article[@id = 'story']//p[@class = 'story-body-text story-content']//text()").extract())
            text = self.__remove_non_ascii_chars(utf8_text)

            article_item = datacollecter.items.ArticleItem()
            article_item['title'] = title
            article_item['text'] = text
            article_item['url'] = response.url
            return article_item
        return None

    def __remove_non_ascii_chars(self, utf8_text):
        utf8_char_string = []
        utf8_char_string.extend(utf8_text)
        return ''.join([char for char in utf8_char_string if ord(char) < 128])
