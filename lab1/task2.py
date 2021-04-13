from scrapy import cmdline
import os
import lxml.etree as etree


def crawl():
    try:
        os.remove("results/petmarket.xml")
    except OSError:
        print("results/petmarket.xml not found")
    cmdline.execute("scrapy crawl petmarket -o results/petmarket.xml -t xml".split())


def xslt_parse():
    dom = etree.parse('results/petmarket.xml')
    xslt = etree.parse('petmarket.xslt')
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    with open('results/petmarket.html', 'wb') as f:
        f.write(etree.tostring(newdom, pretty_print=True))


# crawl()
xslt_parse()