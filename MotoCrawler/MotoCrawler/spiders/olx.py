import datetime
import json
from urllib.parse import urlencode
import scrapy
from scrapy.crawler import CrawlerProcess

from scrapy.selector import Selector


# OnTheMarket scraper class
class OlxScraper(scrapy.Spider):
    #  spider name
    name = 'olx'

    #  base URL
    base_url = 'https://www.olx.pl/motoryzacja/samochody'

    # search query parameters - specify additional info of interest
    params = {
        "page": 1,
        "year_from": "[filter_float_year%3Afrom]=1995",
        "year_to": "[filter_float_year%3Ato]=1999",
    }

    #  headers
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0",
        "referer": base_url
    }

    #  custom download settings
    custom_settings = {
        #  uncomment to set accordingly
        # "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        # "DOWNLOAD_TIMEOUT": 0.25  # 250 ms of delay
    }

    #  current page
    current_page = 1

    #  car (brand, model) tuple list
    cars = []

    #  constructor initializer
    def __init__(self):
        #  init cars content
        content = ''

        #  read cars file
        with open('./input/input.json', 'r') as f:
            for line in f.read():
                content += line

        #  init car (brand, model) list
        for item in json.loads(content):
            self.cars.append((item['brand'], item['model']))

        print(self.cars)

    #  general crawler
    def start_requests(self):

        #  init filename
        filename = './output/Moto_Crawler_' + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M') + '.json'

        #  brands count
        count = 1

        #  loop over cars (brands/models)
        for brand, model in self.cars:
            self.current_page = 1
            next_car = self.base_url + '/' + brand.lower() + '/' + model.lower() + '/'
            yield scrapy.Request(url=next_car, headers=self.headers, meta={
                'brand': brand,
                'model': model,
                'filename': filename,
                'count': count,
            }, callback=self.parse_links)
            count += 1

    #  parse car links
    def parse_links(self, res):
        #  extract forwarded data
        brand = res.meta.get('brand')
        model = res.meta.get('model')
        filename = res.meta.get('filename')
        count = res.meta.get('count')

        #  print Verbose debug info
        print('\n\nCAR <%s %s>: %s out of %s cars' % (brand, model, count, len(self.cars)))

        #  loop over car cards
        for card in res.css('td.offer'):
            listing = card.css('a.detailsLink::attr(href)').get()
            if listing is not None:
                yield res.follow(url=listing, headers=self.headers, meta={
                    'brand': brand,
                    'model': model,
                    'filename': filename,
                    'count': count}, callback=self.parse_listing)
            else:
                continue

    def parse_listing(self, res):
        # extract forwarded data
        brand = res.meta.get('brand')
        model = res.meta.get('model')
        filename = res.meta.get('filename')

        features = {}
        if "olx.pl" in res.url:
            #  extract features
            try:
                features = {
                    'id': res.css('div.clm-samurai::attr(data-item)').get(),

                    'url': res.url,

                    'brand': brand,

                    'model': model,

                    'image_urls': [photo for photo in res.css('ul#descGallery').css('a::attr(href)').getall()],

                    # Star means we also want the element's children.

                    'full_description': res.css('div#textContent *::text').get().strip(),

                }

            except:
                print("Car Extraction Failed")

            # extract script for features
            script = ''.join([script for script in res.css('script').getall() if
                              'GPT.targeting =' in script])
            feature_dict = script.split('GPT.targeting = {')[1][0:300]

            # try to extract features from script or else leave empty
            try:
                features['title'] = feature_dict.split('"ad_title:"')[1].split(',')[0],
            except:
                features['title'] = ''

            try:
                features['city'] = feature_dict.split('"city:"')[1].split(',')[0],
            except:
                features['city'] = ''

            try:
                features['manufacturing_year'] = feature_dict.split('"year:"')[1].split(',')[0],
            except:
                features['manufacturing_year'] = ''

            try:
                features['mileage'] = feature_dict.split('"milage:"')[1].split(',')[0],
            except:
                features['mileage'] = ''

            try:
                features['region'] = feature_dict.split('"region:"')[1].split(',')[0],
            except:
                features['region'] = ''

            try:
                features['gearbox'] = feature_dict.split('"transmission:"')[1].split(',')[0],
            except:
                features['gearbox'] = ''

            try:
                features['enginesize'] = feature_dict.split('"enginesize:"')[1].split(',')[0],
            except:
                features['enginesize'] = ''

            try:
                features['subregion'] = feature_dict.split('"subregion":')[1].split(',')[0],
            except:
                features['subregion'] = ''

            try:
                features['price'] = feature_dict.split('"ad_price:"')[1].split(',')[0],
            except:
                features['price'] = ''

            #  print extraction in terminal - for debugging
            #  print(json.dumps(features, indent=4))

            # write data to JSON file
            with open(filename, 'a') as f:
                f.write(json.dumps(features, indent=4) + '\n')
        else:
            print("Otomoto offer, extraction code to be written.")


#  main driver
if __name__ == "__main__":
    #  run scraper
    process = CrawlerProcess()
    process.crawl(OlxScraper)
    process.start()
