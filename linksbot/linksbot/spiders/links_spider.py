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
        #urls = ["http://insecam.org/en/bycountry/US/", "http://insecam.org/en/bycountry/US/?page=2/", "http://insecam.org/en/bycountry/US/?page=3/", "http://insecam.org/en/bycountry/US/?page=4/", "http://insecam.org/en/bycountry/US/?page=5/", "http://insecam.org/en/bycountry/US/?page=6/", "http://insecam.org/en/bycountry/US/?page=7/", "http://insecam.org/en/bycountry/US/?page=8/", "http://insecam.org/en/bycountry/US/?page=9/", "http://insecam.org/en/bycountry/US/?page=10/", "http://insecam.org/en/bycountry/US/?page=11/", "http://insecam.org/en/bycountry/US/?page=12/"]
        urls = ['http://insecam.org/en/','http://insecam.org/en/byrating/','http://insecam.org/en/mapcity/#','http://insecam.org/en/bytype/Android-IPWebcam/','http://insecam.org/en/bytype/Axis/','http://insecam.org/en/bytype/Axis2/','http://insecam.org/en/bytype/AxisMkII/','http://insecam.org/en/bytype/BlueIris/','http://insecam.org/en/bytype/Bosch/','http://insecam.org/en/bytype/Canon/','http://insecam.org/en/bytype/ChannelVision/','http://insecam.org/en/bytype/Defeway/','http://insecam.org/en/bytype/DLink/','http://insecam.org/en/bytype/DLink-DCS-932/','http://insecam.org/en/bytype/Foscam/','http://insecam.org/en/bytype/FoscamIPCam/','http://insecam.org/en/bytype/Hi3516/','http://insecam.org/en/bytype/Linksys/','http://insecam.org/en/bytype/Megapixel/','http://insecam.org/en/bytype/Mobotix/','http://insecam.org/en/bytype/Motion/','http://insecam.org/en/bytype/Panasonic/','http://insecam.org/en/bytype/PanasonicHD/','http://insecam.org/en/bytype/Sony/','http://insecam.org/en/bytype/Sony-CS3/','http://insecam.org/en/bytype/Streamer/','http://insecam.org/en/bytype/Toshiba/','http://insecam.org/en/bytype/TPLink/','http://insecam.org/en/bytype/Vivotek/','http://insecam.org/en/bytype/WebcamXP/','http://insecam.org/en/bytype/WIFICam/','http://insecam.org/en/bytype/WYM/','http://insecam.org/en/bytype/Yawcam/','http://insecam.org/en/bycountry/US/','http://insecam.org/en/bycountry/KR/','http://insecam.org/en/bycountry/JP/','http://insecam.org/en/bycountry/TW/','http://insecam.org/en/bycountry/IT/','http://insecam.org/en/bycountry/RU/','http://insecam.org/en/bycountry/DE/','http://insecam.org/en/bycountry/FR/','http://insecam.org/en/bycountry/AT/','http://insecam.org/en/bycountry/IR/','http://insecam.org/en/bycountry/CZ/','http://insecam.org/en/bycountry/CH/','http://insecam.org/en/bycountry/VN/','http://insecam.org/en/bycountry/ES/','http://insecam.org/en/bycountry/NL/','http://insecam.org/en/bycountry/BE/','http://insecam.org/en/bycountry/BR/','http://insecam.org/en/bycountry/GB/','http://insecam.org/en/bycountry/CA/','http://insecam.org/en/bycountry/SE/','http://insecam.org/en/bycountry/IN/','http://insecam.org/en/bycountry/RO/','http://insecam.org/en/bycountry/PL/','http://insecam.org/en/bycountry/NO/','http://insecam.org/en/bycountry/BG/']
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
            if 'http' in currentlink and '.com' not in currentlink and '.ru' not in currentlink and '.net' not in currentlink and '.jpg' not in currentlink and '.jpeg' not in currentlink and '.png' not in currentlink  and '.me' not in currentlink and '.gif' not in currentlink and '.co' not in currentlink:
                if currentlink in linkstoscrapelist:
                    pass
                elif currentlink not in linkstoscrapelist:
                    print(currentlink)
                    cameralinks.append(currentlink)
                    global linkstxt
                    with open("links.txt","a") as linkstxt:
                        linkstxt.writelines(currentlink + '\n')
                else:
                    pass
                #print(currentlink)
            #elif 'http' in currentlink:
            #    print(currentlink)
            #    linkstoscrapelist.append(currentlink)
            else:
                pass

        for link in linkstoscrapelist:
            #i = i + 1
            #if i == 150:
            #    pass
            #else:
            yield scrapy.Request(link, callback=self.parse)
#linkstxt.close()
