from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from tutorial.items import OperaSportsMatchItem
from scrapy import Request

class OperaSportsSpider(Spider):
    name = "opera_sports"
    allowed_domains = ["sports.opera.com"]
   
    start_urls = [
       "http://sports.opera.com/?sport=soccer&page=competition&id=8&p=-2&localization_id=www",
       "http://sports.opera.com/?sport=soccer&page=competition&id=91&p=-6&localization_id=www",
       "http://sports.opera.com/?sport=soccer&page=competition&id=33&p=-24&localization_id=www"

    ]


    def parse(self, response):
        sel = Selector(response)
        matches = sel.xpath('//div[contains(@id,"block_competition_matches")]//tr')
        items = []
        for match in matches:
             
            home_team = match.xpath('td[contains(@class,"team team-a ")]//a/@title').extract()[0]
            away_team = match.xpath('td[contains(@class,"team team-b ")]//a/@title').extract()[0]
            score = match.xpath('td[contains(@class,"score-time score")]//a/text()').extract()[0]
            hour = match.xpath('td[contains(@class,"score-time status")]//span/text()').extract()[0]
            date = match.xpath('td[contains(@class,"date no-repetition")]/text()').extract()[0]

            if not score:
                score = ""
            else:   
                score = score.strip();

            if not hour:
                hour = ""
            else:   
                hour = hour.strip();    
                    

            season = ''.join(sel.xpath('//div[contains(@id,"block_competition_nav_")]//option[contains(@selected,"selected")]/text()').extract())

            if  home_team and away_team:
                item = OperaSportsMatchItem()
                item['home_team'] = home_team
                item['away_team'] = away_team
                item['hour'] = hour
                item['score'] = score
                item['season'] = season
                item['date'] = date
                yield item
              
        next_page = sel.xpath('//div[contains(@id,"block_competition_matches_")]//span[contains(@class,"nav_description")]//a[contains(@class,"next")]/text()').extract()

        if not "disabled" in next_page:
            url = response.urljoin(sel.xpath('//div[contains(@id,"block_competition_matches_")]//span[contains(@class,"nav_description")]//a[contains(@class,"next")]/@href').extract()[0])
            yield Request(url, self.parse)      
        