import scrapy
import re
import bs4
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from datetime import date

class LinksSpider(scrapy.Spider):
    name = "linkspider"
    global linkstoscrapelist
    linkstoscrapelist = []
    global cameralinks
    cameralinks = []

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'DOWNLOAD_DELAY': 0.25,
        'AUTOTHROTTLE_ENABLED': False,
        'LOG_ENABLED': False
    }
    def start_requests(self):
        urls = ["http://insecam.org/en/bycountry/US/", "http://insecam.org/en/bycountry/US/?page=2/", "http://insecam.org/en/bycountry/US/?page=3", "http://insecam.org/en/bycountry/US/?page=4", "http://insecam.org/en/bycountry/US/?page=5/", "http://insecam.org/en/bycountry/US/?page=6"]

        for url in urls:
            #print('here')
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")

        for a in soup.find_all('a', href=True):
            currentlink = str(a['href'])
            if 'http' in currentlink:
                #print(currentlink)
                linkstoscrapelist.append(currentlink)
                #print(currentlink)
            #elif 'http' in currentlink:
            #    print(currentlink)
            #    linkstoscrapelist.append(currentlink)
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
                #print(currentlink)
            #elif 'http' in currentlink:
            #    print(currentlink)
            #    linkstoscrapelist.append(currentlink)
            else:
                pass

        for link in linkstoscrapelist:
            i = i + 1
            if i == 150:
                pass
            else:
                yield scrapy.Request(link, callback=self.parse)
#linkstxt.close()