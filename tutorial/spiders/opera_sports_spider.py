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
             
            home_team = match.xpath('td[contains(@class,"team team-a ")]//a/@title').extract()
            away_team = match.xpath('td[contains(@class,"team team-b ")]//a/@title').extract()
            score = match.xpath('td[contains(@class,"score-time score")]//a/text()').extract()
            hour = match.xpath('td[contains(@class,"score-time status")]//a/text()').extract()

            if not score:
                score = ""
            else:   
                score = score[0].strip();

            if not hour:
                hour = ""
            else:   
                hour = hour[0].strip();    
                    

            season = sel.xpath('//div[contains(@id,"block_competition_nav_375888a5768887cc1e3df4571a8a147f")]//option[contains(@selected,"selected")]/text()').extract()

            if  home_team and away_team:
                item = OperaSportsMatchItem()
                item['home_team'] = home_team
                item['away_team'] = away_team
                item['hour'] = hour
                item['score'] = score
                item['season'] = season
                items.append(item)

        return items