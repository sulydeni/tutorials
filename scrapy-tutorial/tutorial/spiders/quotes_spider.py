import scrapy
from scrapy.linkextractors import LinkExtractor

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        urls = [
            #'https://www.walmart.com/browse/electronics/all-laptop-computers/3944_3951_1089430_132960',
            'https://www.walmart.com/browse/electronics/all-laptop-computers/3944_3951_1089430_132960?page=3#searchProductResult',
            #'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,meta={
    'splash': {
        'args': {
            # set rendering arguments here
            'html': 1,
            'png': 1,
            'wait': 5

            # 'url' is prefilled from request url
            # 'http_method' is set to 'POST' for POST requests
            # 'body' is set to request body for POST requests
        },

        # optional parameters
        #'endpoint': 'render.json',  # optional; default is render.json
    }
})

    def parse(self, response):
        self.log(response.text)
        self.log(response.status)
        le = LinkExtractor()
        for link in le.extract_links(response):
            if '/ip/' in link.url:
                self.log('url found!' + link.url)
                yield {
                    'product_url':link.url
                }
            else:
                self.log('silly found!' + link.url)
                #yield {
                #    'product_url':link.url
                #}
                
#        for quote in response.css('div.quote'):
#            yield {
#                'text': quote.css('span.text::text').extract_first(),
#                'author': quote.css('small.author::text').extract_first(),
#                'tags': quote.css('div.tags a.tag::text').extract(),
#            }