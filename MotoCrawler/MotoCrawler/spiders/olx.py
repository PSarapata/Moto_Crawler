import datetime
import json
import scrapy
from scrapy.crawler import CrawlerProcess

# I had some problem with imports, you might not need it
import repackage
repackage.up()
# Import custom Scrapy item, which then gets fed into pipelines for processing:
from items import MotocrawlerItem


# olx scraper class
class OlxScraper(scrapy.Spider):
    """Spider for scraping Polish automotive website, offers two output options - stores offers either in json file
    or save in your database. Simply uncomment filename references if you prefer the first option.
    Keep in mind that this website shows offers from another portal as well.

    WARNING: Those websites implemented extensive security measures. Do not produce too many consecutive requests or
    you will get banned. You might also find that your data output is different than expected. I believe that is also
    due to some hidden JS script, which were meant to protect from data scraping.
    My advice - if you don't need this spider - don't use it.
    """

    #  spider name
    name = 'olx'

    #  base URL
    base_url = 'https://www.olx.pl/motoryzacja/samochody'

    # search query parameters - specify additional points of interest/narrow down your search
    params = {
        "page": 1,
        "price_to": "search[filter_float_price%3Ato]=20000",
        "year_from": "search[filter_float_year%3Afrom]=1995",
        "year_to": "search[filter_float_year%3Ato]=1999",
    }

    #  headers
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_2_1 like Mac OS X; sl-SI) AppleWebKit/533.1.6 (KHTML, like Gecko) Version/3.0.5 Mobile/8B115 Safari/6533.1.6",
        "referer": base_url
    }

    #  custom download settings
    custom_settings = {
         # Set accordingly. Advise: do not shorten delay for those websites.
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_TIMEOUT": 2  # 2 s of delay
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
        """Initiates crawling. Yields a scrapy request -> redirects to list view with brand/model instance,
        then calls in parse_links on the request.
        :return: yields a request to url with the list of offers, for each car in the input file.
        Then, makes a callback to parse_links method."""
        #  init filename
        # filename = './output/Moto_Crawler_OLX_' + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M') + '.json'

        #  brands count
        count = 1

        #  loop over cars (brands/models)
        for brand, model in self.cars:
            self.current_page = 1
            next_car = self.base_url + '/' + brand.lower() + '/' + model.lower() + '/'
            if model == "Eclipse":
                next_car += '?' + self.params["price_to"] + '&' + self.params["year_from"] + '&' \
                            + self.params["year_to"]
            yield scrapy.Request(url=next_car, headers=self.headers, meta={
                'brand': brand,
                'model': model,
                # 'filename': filename,
                'count': count,
            }, callback=self.parse_links)
            count += 1

    #  parse car links
    def parse_links(self, res):
        """Extracts url of all listed offers, including pagination, calls in parse_listing on each offer URL.
        :return: yields url for the offer and calls parse_listing method."""

        #  extract forwarded data
        brand = res.meta.get('brand')
        model = res.meta.get('model')
        # filename = res.meta.get('filename')
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
                    # 'filename': filename,
                    'count': count}, callback=self.parse_listing)
            else:
                continue

        try:
            #  handle pagination
            self.current_page += 1
            try:
                total_pages = int(res.css('a[data-cy="page-link-last"]::attr(href)').get().split('page=')[1])
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
                    # 'filename': filename,
                    'count': count}, callback=self.parse_links)
        except:
            pass

    def parse_listing(self, res):
        """Extracts information from listing (offer) details.
        On success, yields a Scrapy MotoCrawlerItem instance,
        which is then processed by the DatabasePipeline.
        :return: custom Scrapy MotoCrawlerItem, which is then fed into DatabasePipeline"""

        # extract forwarded data
        brand = res.meta.get('brand')
        model = res.meta.get('model')
        # filename = res.meta.get('filename')

        features = {}
        if "olx.pl" in res.url:
            #  extract features for olx offer
            try:
                features = {
                    'id': res.css('div.clm-samurai::attr(data-item)').get(),

                    'url': res.url,

                    'brand': brand,

                    'model': model,

                    'image_urls': [photo for photo in res.css('ul#descGallery').css('a::attr(href)').getall()],

                    # Star means we also want the element's children.

                    'full_description': '\n'.join([line.strip().replace('\r', '') for line in res.css(
                        'div#textContent *::text').getall()])

                }

            except:
                print("Car Extraction Failed")

            # extract script for features
            script = ''.join([script for script in res.css('script').getall() if
                              "GPT.targeting =" in script])
            feature_dict = script.split('GPT.targeting = {')[1][0:1000]

            # try to extract features from script or else leave empty
            try:
                features['title'] = feature_dict.split('"ad_title"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['title'] = ''

            try:
                features['city'] = feature_dict.split('"city"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['city'] = ''

            try:
                features['manufacturing_year'] = feature_dict.split('"year"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['manufacturing_year'] = ''

            try:
                features['mileage'] = feature_dict.split('"milage"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['mileage'] = ''

            try:
                features['region'] = feature_dict.split('"region"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['region'] = ''

            try:
                features['gearbox'] = feature_dict.split('"transmission"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['gearbox'] = ''

            try:
                features['enginesize'] = feature_dict.split('"enginesize"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['enginesize'] = ''

            try:
                features['subregion'] = feature_dict.split('"subregion"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['subregion'] = ''

            try:
                features['price'] = feature_dict.split('"ad_price"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['price'] = ''

            #  print extraction in terminal - for debugging
            #  print(json.dumps(features, indent=4))
            # write data to JSON file
            # with open(filename, 'a') as f:
            #     f.write(json.dumps(features, indent=4) + '\n')

            # write data to Database
            motocrawler_item = MotocrawlerItem(
                url=features['url'],
                brand=features['brand'],
                model=features['model'],
                title=features['title'],
                price=features['price'],
                description=features.get('full_description'),
                photos=features.get('image_urls')
            )
            yield motocrawler_item

        elif "otomoto.pl" in res.url:
            #  extract features for otomoto offer
            try:
                features = {
                    'id': res.css('span#ad_id::text').get(),

                    'url': res.url,

                    'brand': brand,

                    'model': model,

                    'image_urls': [image for image in res.css('img.bigImage::attr(data-lazy)').getall()],

                    # Star means we also want the element's children.

                    'full_description': '\n'.join([line.strip().replace('\r', '') for line in res.css(
                        'div.offer-description__description *::text').getall()])

                }
            except:
                print('Failed to extract otomoto features')

            # extract script for features
            script = ''.join([script for script in res.css('script').getall() if
                              "GPT.targeting =" in script])
            feature_dict = script.split('GPT.targeting = {')[1][0:1000]

            # try to extract features from script or else leave empty
            try:
                features['title'] = feature_dict.split('"ad_title"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['title'] = ''

            try:
                features['city'] = feature_dict.split('"city"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['city'] = ''

            try:
                features['manufacturing_year'] = feature_dict.split('"year"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['manufacturing_year'] = ''

            try:
                features['mileage'] = feature_dict.split('"mileage"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['mileage'] = ''

            try:
                features['region'] = feature_dict.split('"region"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['region'] = ''

            try:
                features['gearbox'] = feature_dict.split('"transmission"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['gearbox'] = ''

            try:
                features['enginesize'] = feature_dict.split('"enginesize"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['enginesize'] = ''

            try:
                features['subregion'] = feature_dict.split('"subregion"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['subregion'] = ''

            try:
                features['price'] = feature_dict.split('"ad_price"')[1].split(':')[1].split(',')[0].split('"')[1],
            except:
                features['price'] = ''

            # write data to JSON file
            # with open(filename, 'a') as f:
            #     f.write(json.dumps(features, indent=4) + '\n')

            # write data to Database
            motocrawler_item = MotocrawlerItem(
                url=features['url'],
                brand=features['brand'],
                model=features['model'],
                title=features['title'],
                price=features['price'],
                description=features.get('full_description'),
                photos=features.get('image_urls')
            )
            yield motocrawler_item
        else:
            print(Exception("Something has gone wrong."))


#  main driver
if __name__ == "__main__":
    #  run scraper
    process = CrawlerProcess()
    process.crawl(OlxScraper)
    process.start()
