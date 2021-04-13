import scrapy

def isNotEmptyString(str):
    return len(str) > 0

class GolosuaSpider(scrapy.Spider):
    name = "golosua"
    custom_settings = {
        'ITEM_PIPELINES': {
            'lab1.pipelines.Lab1Pipeline': 300,
        }
    }
    fields = {
        'img': '//img/@src',
        'text': '//*[not(self::script)][not(self::style)]/text()',
        'link': '//a/@href'
    }
    start_urls = [
        'https://golos.ua'
    ]
    allowed_domains = [
        'golos.ua'
    ]

    def parse(self, response):
        text = filter(isNotEmptyString,
                      map(lambda str: str.strip(),
                          [text.extract() for text in response.xpath(self.fields["text"])]))
        images = map(lambda url: ((response.url + url) if url.startswith('/') else url),
                     [img_url.extract() for img_url in response.xpath(self.fields["img"])])
        yield {
            'text': text,
            'images': images,
            'url': response.url
        }
        for link_url in response.xpath(self.fields['link']):
            yield response.follow(link_url.extract(), callback=self.parse)
