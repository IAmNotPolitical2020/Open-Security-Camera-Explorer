import scrapy
import re
import bs4
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from datetime import date
import random

class LinksSpider(scrapy.Spider):
    name = "linkspider"
    global linkstoscrapelist
    linkstoscrapelist = []
    global cameralinks
    cameralinks = []
    global urls
    urls = []

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'DOWNLOAD_DELAY': 0.25,
        'AUTOTHROTTLE_ENABLED': False,
        'LOG_ENABLED': False
    }
    def start_requests(self):

        with open('websites.txt','r') as f:
            lines = f.readlines()
            for line in lines:
                urls.append(line)
        for i in range(10):
            yield scrapy.Request(url=random.choice(urls), callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")

        for a in soup.find_all('a', href=True):
            currentlink = str(a['href'])
            if 'http' in currentlink:
                linkstoscrapelist.append(currentlink)
            else:
                pass

        for a in soup.find_all('img'):
            currentlink = str(a['src'])
            if 'http' in currentlink and '.com' not in currentlink and '.ru' not in currentlink and '.net' not in currentlink:
                print(currentlink)
                cameralinks.append(currentlink)
                global linkstxt
                with open("links.txt","a") as linkstxt:
                    linkstxt.writelines(currentlink + '\n')
            else:
                pass

        for link in linkstoscrapelist:
            i = i + 1
            if i == 150:
                pass
            else:
                yield scrapy.Request(link, callback=self.parse)
