from scrapy.spiders import Spider
from scrapy.selector import Selector
from tutorial.items import OperaSportsMatchItem


class OperaSportsSpider(Spider):
    name = "opera_sports"
    allowed_domains = ["sports.opera.com"]
    start_urls = [
        "http://sports.opera.com/?sport=soccer&page=competition&id=8&p=0&localization_id=www",
    ]

    def parse(self, response):
        sel = Selector(response)
        matches = sel.xpath('//div[contains(@id,"block_competition_matches_304a33487b604ee39ff8538c139dc0a0")]//tr')
        items = []
        for match in matches:
            item = OperaSportsMatchItem()
            item['home_team'] = site.xpath('//td[contains(@class,"team team-a ")]//a/@title').extract()
            item['away_team'] = site.xpath('//td[contains(@class,"team team-b ")]//a/@title').extract()
            items.append(item)
        return items