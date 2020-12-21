import datetime
import json
from urllib.parse import urlencode
import scrapy
from scrapy.crawler import CrawlerProcess

from scrapy.selector import Selector


# OnTheMarket scraper class
class AutoScoutScraper(scrapy.Spider):
    #  spider name
    name = 'autoscout'

    #  base URL
    base_url = 'https://www.autoscout24.pl'

    # search query parameters - specify additional info of interest
    params = {
        "page": 1,
        "price_to": "priceto=3000",
        "year_from": "fregfrom=1995",
        "year_to": "fregto=2000",
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
        filename = './output/Moto_Crawler_AutoScout_' + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M') + '.json'

        #  brands count
        count = 1

        #  loop over cars (brands/models)
        for brand, model in self.cars:
            self.current_page = 1
            next_car = self.base_url + '/lst/' + brand.lower() + '/' + model.lower()
            if model == "Eclipse":
                next_car += '?page=' + str(self.params["page"]) + '&' + self.params["price_to"] + '&' \
                            + self.params["year_from"] + '&' + self.params["year_to"]
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
        print('\n\nCAR %s: %s out of %s cars' % (brand, count, len(self.cars)))

        #  loop over car cards
        for card in res.css('div.cldt-summary-titles'):
            listing = card.css('a::attr(href)').get()
            yield res.follow(url=listing, headers=self.headers, meta={
                'brand': brand,
                'model': model,
                'filename': filename,
                'count': count}, callback=self.parse_listing)

        try:
            #  handle pagination
            self.current_page += 1
            try:
                total_pages = int(res.css('div.cl-refine-search-btn-container').css('a::attr(href)').get().split(
                    'size=')[1].split('&')[0])
            except:
                total_pages = 1
                print('Exception')

            # create next page link
            self.params['page'] = self.current_page
            next_page = self.base_url + brand.lower() + '/' + model.lower + '/?page=' + str(self.params['page'])

            #  handle pagination
            if self.current_page <= total_pages:
                #  print debug info
                print('\n\n %s | %s \n\n' % (int(self.current_page), total_pages))

                #  crawl more cars
                yield res.follow(url=next_page, headers=self.headers, meta={
                    'brand': brand,
                    'model': model,
                    'filename': filename,
                    'count': count}, callback=self.parse_links)
        except:
            pass

    #  parse car listings
    def parse_listing(self, res):
        # extract forwarded data
        brand = res.meta.get('brand')
        model = res.meta.get('model')
        filename = res.meta.get('filename')

        try:
            features = {
                'id': res.css('a::attr(data-classified-guid)').get(),

                'url': res.url,

                'brand': brand,

                'model': model,

                'title': res.css('h2.as24-pictures__picture-title::text').get(),

                'city': res.css('div.cldt-stage-vendor-text').css('span.sc-font-bold::text').get(),

                'price': res.css('div.cldt-price').css('h2::text').get().strip(),

                'contact_seller': res.css('div.cldt-vendor-phones').css('a::attr(href)').get(),

                'image_urls': [res.css('div.gallery-picture').css('img::attr(src)').get()] + ([Selector(
                    text=img).css('img::attr(data-src)').get() for img in res.css('div.gallery-picture').getall()][1:]),


                'feature_list': list(set(['<li>' + Selector(text=li).css('span.cldt-stage-highlight::text').get() +
                                          '</li>' for li in res.css('div.cldt-stage-highlights').css(
                        'span.cldt-stage-highlight').getall()])),

            }

            # attempt to extract car attributes
            script = res.css('s24-ad-targeting::text').get()

            try:
                features['manufacturing_year'] = script.split('"styea"')[1].split(': ')[1].split(',')[0]
            except:
                features['manufacturing_year'] = ''

            try:
                features['power'] = script.split('"sthp"')[1].split(': ')[1].split(',')[0]
            except:
                features['power'] = ''

            try:
                features['mileage'] = script.split('"stmil"')[1].split(': ')[1].split(',')[0]
            except:
                features['mileage'] = ''

            try:
                features['gearbox'] = script.split('"gear"')[1].split(': ')[1].split(',')[0]
            except:
                features['gearbox'] = ''

            try:
                features['engine_capacity'] = script.split('"stccm"')[1].split(': ')[1].split(',')[0]
            except:
                features['engine_capacity'] = ''

        except:
            print("Car Extraction Failed")

        # write data to JSONL file
        with open(filename, 'a') as f:
            f.write(json.dumps(features, indent=4) + '\n')


#  main driver
if __name__ == "__main__":
    #  run scraper
    process = CrawlerProcess()
    process.crawl(AutoScoutScraper)
    process.start()
