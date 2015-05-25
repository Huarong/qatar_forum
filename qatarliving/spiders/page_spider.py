import scrapy

from qatarliving.items import QatarlivingItem


def load_urls(path):
    urls = []
    if type(path) == str:
        with open(path) as f:
            urls = ['http://www.qatarliving.com%s' % line.rstrip() for line in f.readlines()]
            return urls
    elif type(path) == list:
        for p in path:
            with open(p) as f:
                for line in f:
                    urls.append('http://www.qatarliving.com%s' % line.rstrip())
        return urls
    else:
        raise ValueError('invalid parameter type: %s' % path)


class PageSpider(scrapy.spider.Spider):
    name = "Page"
    allowed_domains = ["qatarliving.com"]

    sectors = ['company-news',
             'pets-animals',
             'movies-qatar',
             'environment',
             'qatar-2022',
             'ramadan',
             'news',
             'dining',
             'beauty-style',
             'opportunities',
             'recipes',
             'qatari-culture',
             'missing-home',
             'electronics-0',
             'salary-allowances',
             'qatar-living-website',
             'technology',
             'fashion',
             'computers-internet',
             'language',
             'health-fitness',
             'politics']

    start_urls = load_urls(['urls/%s' % e for e in sectors])

    def parse(self, response):
        sel = response.selector
        item = QatarlivingItem()
        item['url'] = response.url
        item['title'] = sel.xpath('//*[@id="page-title"]/text()').extract()[0]
        item['subtitle'] = ' '.join(sel.xpath('//*[@id="node-body"]/div/div[3]/p/text()').extract())
        item['comments'] = sel.xpath('//*[@id="comments"]/div/article/div[@class="post-comment"]/div/p/text()').extract()
        yield item

