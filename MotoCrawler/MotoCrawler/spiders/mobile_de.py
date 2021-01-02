import datetime
import json
import scrapy
from scrapy.crawler import CrawlerProcess

# I had some problem with imports, you might not need it
import repackage
repackage.up()
from items import MotocrawlerItem


# mobile_de Scraper scraper class
class MobileDeScraper(scrapy.Spider):
    """Spider for scraping German automotive website, offers two output options - stores offers either in json file
    or save in your database. Simply uncomment filename references if you prefer the first option."""
    #  spider name
    name = 'mobile_de'

    #  base URL
    base_url = 'https://www.mobile.de/pl/'

    # search query parameters - specify additional info of interest
    params = {
        "vhc": "car",
        "pgn": "1",
        "pgs": "10",
        "srt": "price",
        "sro": "asc",
        "ms1": "17700_9_",
        "prx": "3000",
    }

    #  query string to pass parameters into URL
    mconfig = []
    for k, v in params.items():
        mconfig.append(str(k) + ':' + str(v))
    query_str = ','.join(mconfig)

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
        # filename = './output/Moto_Crawler_MobileDe_' + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M') + '.json'

        #  brands count
        count = 1

        #  loop over cars (brands/models)
        for brand, model in self.cars:
            self.current_page = 1
            next_car = self.base_url + 'samochod/' + brand.lower() + '-' + model.lower() + '/' + self.query_str
            yield scrapy.Request(url=next_car, headers=self.headers, meta={
                'brand': brand,
                'model': model,
                # 'filename': filename,
                'count': count,
            }, callback=self.parse_links)
            count += 1

    #  parse car links
    def parse_links(self, res):
        #  extract forwarded data
        brand = res.meta.get('brand')
        model = res.meta.get('model')
        # filename = res.meta.get('filename')
        count = res.meta.get('count')

        #  print Verbose debug info
        print('\n\nCAR %s: %s out of %s cars' % (brand, count, len(self.cars)))

        #  loop over car cards
        for card in res.css('div.result-list-section').css('article.list-entry'):
            listing = card.css('a.vehicle-data::attr(href)').get()
            yield res.follow(url=('https://www.mobile.de' + listing), headers=self.headers, meta={
                'brand': brand,
                'model': model,
                # 'filename': filename,
                'count': count}, callback=self.parse_listing)

        try:
            #  handle pagination
            self.current_page += 1
            try:
                total_pages = int(res.css('span.pagination-page-numbers').css('a::text').getall()[-1])
            except:
                total_pages = 1
                print('Exception')

            # create next page link
            self.params['pgn'] = str(self.current_page)
            next_page = self.base_url + brand.lower() + '/' + model.lower + '/' + self.query_str

            #  handle pagination
            if self.current_page <= total_pages:
                #  print debug info
                print('\n\n %s | %s \n\n' % (int(self.current_page), total_pages))

                #  crawl more cars
                yield res.follow(url=next_page, headers=self.headers, meta={
                    'brand': brand,
                    'model': model,
                    # 'filename': filename,
                    'count': count}, callback=self.parse_links)
        except:
            pass

    #  parse car listings
    def parse_listing(self, res):
        # extract forwarded data
        brand = res.meta.get('brand')
        model = res.meta.get('model')
        # filename = res.meta.get('filename')

        try:
            features = {
                'id': res.url.split('/')[-1].split('.html')[0],

                'url': res.url,

                'brand': brand,

                'model': model,

                'title': res.css('h1.g-col-8::text').get(),

                'city': res.css('div.g-col-m-6').css('span::text').get(),

                'price': res.css('span.netto-price::text').get(),

                'image_urls': res.css('div.js-gallery-img-wrapper').css('div.gallery-bg::attr(data-src)').getall(),

            }

            # attempt to extract car attributes
            script = res.css('div.attributes-box').css(
                    'span.g-col-6::text').getall()

            try:
                features['manufacturing_year'] = script[(script.index('Pierwsza rejestracja') + 1)]
            except:
                features['manufacturing_year'] = ''

            try:
                features['power'] = script[(script.index('Moc') + 1)]
            except:
                features['power'] = ''

            try:
                features['mileage'] = script[(script.index('Przebieg') + 1)]
            except:
                features['mileage'] = ''

            try:
                features['gearbox'] = script[(script.index('Skrzynia biegów') + 1)]
            except:
                features['gearbox'] = ''

            try:
                features['fuel'] = script[(script.index('Paliwo') + 1)]
            except:
                features['fuel'] = ''

            try:
                features['engine_capacity'] = script[(script.index('Pojemność') + 1)]
            except:
                features['engine_capacity'] = ''

            try:
                features['color'] = script[(script.index('Kolor') + 1)]
            except:
                features['color'] = ''

            try:
                features['feature_list'] = [feature for feature in res.css('p.bullet-point-text::text').getall()]
            except:
                features['feature_list'] = ''

            try:
                features['description'] = res.css('div.description-text::text').get()
            except:
                features['description'] = ''

        except:
            print("Car Extraction Failed")

        # write data to JSONL file
        # with open(filename, 'a') as f:
        #     f.write(json.dumps(features, indent=4) + '\n')

        # write data to Database
        motocrawler_item = MotocrawlerItem(
            url=features['url'],
            brand=features['brand'],
            model=features['model'],
            title=features['title'],
            price=features['price'],
            description=features['full_description']
        )
        yield motocrawler_item


#  main driver
if __name__ == "__main__":
    #  run scraper
    process = CrawlerProcess()
    process.crawl(MobileDeScraper)
    process.start()
