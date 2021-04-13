# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from lxml import etree


class Lab1Pipeline:
    def open_spider(self, spider):
        self.root = etree.Element('data')

    def close_spider(self, spider):
        with open('results/golosua.xml', 'wb') as file:
            etree.ElementTree(self.root).write(file, pretty_print=True, encoding="UTF-8")
            
        pagesCount = self.root.xpath('count(//page)')
        textFragmentsCount = self.root.xpath('count(//fragment[@type="text"])')
        print('\033[94m' + '\nAverage count of text fragments per page ' + str(textFragmentsCount / pagesCount) + '\033[0m' + '\n')


    def process_item(self, item, spider):
        page = etree.SubElement(self.root, 'page', url=item['url'])
        for text in item['text']:
            etree.SubElement(page, 'fragment', type='text').text = text
        for url in item['images']:
            etree.SubElement(page, 'fragment', type='image').text = url
        return item
