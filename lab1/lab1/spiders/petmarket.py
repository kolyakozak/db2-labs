import scrapy


class PetmarketSpider(scrapy.Spider):
    name = 'petmarket'
    fields = {
        'link_category': '//div[@class="catalogCard-main-b"]//a/@href',
        'product': '//div[@class="catalogCard-main-b"]',
        'price': './/div[@class="catalogCard-priceBox"]/div/text()',
        'name': './/div[@class="catalogCard-title"]/a/text()',
        'img': './/div[@class="catalogCard-image-i"]/img/@src',
        'product_link': './/div[@class="catalogCard-title"]/a/@href'
    }
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 0,
        'CLOSESPIDER_ITEMCOUNT': 20
    }
    start_urls = [
        'https://petmarket.ua/zootovary-dlja-ryb',
        'https://petmarket.ua/zootovary-dlja-sobak',
        'https://petmarket.ua/tovary-koshek/'
    ]
    allowed_domains = [
        'petmarket.ua'
    ]

    def parse(self, response):
        for a in response.xpath(self.fields["link_category"]):
            yield response.follow(a.extract(), callback=self.parse_products)


    def parse_products(self, response):
        for product in response.xpath(self.fields["product"]):
            yield {
                'link': 'https://petmarket.ua' + product.xpath(self.fields['product_link']).extract()[0],
                'price': product.xpath(self.fields['price']).get().strip(),
                'img': 'https://petmarket.ua' +  product.xpath(self.fields['img']).extract()[0],
                'name': ''.join(product.xpath(self.fields['name']).extract())
            }
