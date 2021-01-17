import datetime
import json
import scrapy
from scrapy.crawler import CrawlerProcess

# I had some problem with imports, you might not need it
import repackage
repackage.up()
# Import custom Scrapy item, which then gets fed into pipelines for processing:
from items import MotocrawlerItem


# sprzedajemy scraper class
class SprzedajemyScraper(scrapy.Spider):
    """Spider for scraping Polish automotive website, offers two output options - stores offers either in json file
    or save in your database. Simply uncomment filename references if you prefer the first option."""
    #  spider name
    name = 'sprzedajemy'

    #  base URL
    base_url = 'https://sprzedajemy.pl/motoryzacja/samochody-osobowe'

    # search query parameters - pagination on this website is based on offset.
    params = {
        "offset": 0
    }

    #  headers
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X; en-US) AppleWebKit/534.37.6 (KHTML, like Gecko) Version/4.0.5 Mobile/8B116 Safari/6534.37.6",
        "referer": base_url
    }

    #  custom download settings
    custom_settings = {
        #  uncomment to set accordingly
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_TIMEOUT": 1  # 1 s of delay
    }

    #  current offset
    current_offset = 0

    #  car (brand, model) tuple list
    cars = []

    #  constructor initializer
    def __init__(self):
        #  init car content
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
        # filename = './output/Moto_Crawler_Sprzedajemy_' + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M') + '.json'

        #  brands count
        count = 1

        #  loop over cars (brands/models)
        for brand, model in self.cars:
            self.current_offset = 0
            next_car = self.base_url + '/' + brand.lower() + '/' + model.lower()
            yield scrapy.Request(url=next_car, headers=self.headers, meta={
                'brand': brand,
                'model': model,
                # 'filename': filename,
                'count': count
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
        print('\n\nCAR %s: %s out of %s cars' % (brand, count, len(self.cars)))

        #  loop over car cards
        for card in res.css('article.element'):
            listing = card.css('a.offerLink::attr(href)').get()
            yield res.follow(url=listing, headers=self.headers, meta={
                'brand': brand,
                'model': model,
                # 'filename': filename,
                'count': count}, callback=self.parse_listing)

        try:
            #  handle pagination --> change offset to set how many cars per page to display
            self.current_offset += 30
            try:
                total_cars = int(res.css('div.cntItemCounter').css('strong::text').get().split('-')[1])
            except:
                total_cars = 1
                print('Exception')

            # create next page link
            self.params['offset'] = self.current_offset
            next_page = self.base_url + brand.lower() + '/' + model.lower + '?offset=' + str(self.params['offset'])

            #  handle pagination
            if self.current_offset < total_cars:
                #  print debug info
                print('\n\n %s | %s \n\n' % (int(self.current_offset), total_cars))

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
        """Extracts information from listing (offer) details.
        On success, yields a Scrapy MotoCrawlerItem instance,
        which is then processed by the DatabasePipeline.
        :return: custom Scrapy MotoCrawlerItem which is then fed into DatabasePipeline"""

        # extract forwarded data
        brand = res.meta.get('brand')
        model = res.meta.get('model')
        # filename = res.meta.get('filename')

        try:
            features = {
                'id': res.css('ul.offerAdditionalInfo').css('a.locationName::attr(data-id)').get(),

                'url': res.url,

                'brand': brand,

                'model': model,

                'title': res.css('span.isUrgentTitle::text').get(),

                'city': res.css('ul.offerAdditionalInfo').css('a.locationName::text').get(),

                'voivodship': res.css('span.province').css('a::text').get(),

                'price': res.css('span[itemprop="price"]::text').get().replace('None', '').strip(),

                'contact_seller': res.css('span.phone-number-truncated::attr(data-phone-end)').get()
                                  + ' ' +
                                  res.css('span.phone-number-truncated').css('span::text').getall()[1],

                'image_urls': res.css('img.js-gallerySlide::attr(src)').getall(),

                # Star means we also want the element's children.

                'full_description': res.css('div.offerDescription').css('span *::text').get(),

                'extra_info': res.css('ul.additional-parameters').css('span::text').getall(),

            }

            #  attempt to extract additional information
            attribute_list = res.css('ul.attribute-list').css('li.item').getall()

            # attempt to extract car attributes
            for item in attribute_list:
                try:
                    if item.split('<span>')[1].split('</span>')[0] == "Rok produkcji":
                        features['manufacturing_year'] = item.split('<strong>')[1].split(' ')[0]
                except:
                    features['manufacturing_year'] = ''

                try:
                    if item.split('<span>')[1].split('</span>')[0] == "Moc":
                        features['power'] = item.split('<strong>')[1].split(' ')[0]
                except:
                    features['power'] = ''

                try:
                    if item.split('<span>')[1].split('</span>')[0] == "Przebieg":
                        features['mileage'] = item.split('<strong>')[1].split(' ')[0]
                except:
                    features['mileage'] = ''

                try:
                    if item.split('<span>')[1].split('</span>')[0] == "Skrzynia biegów":
                        features['gearbox'] = item.split('<strong>')[1].split(' ')[0]
                except:
                    features['gearbox'] = ''

                try:
                    if item.split('<span>')[1].split('</span>')[0] == "Pojemność silnika":
                        features['engine_capacity'] = item.split('<strong>')[1].split(' ')[0]
                except:
                    features['engine_capacity'] = ''

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
            description=features.get('full_description'),
            photos=features.get('image_urls')
        )
        yield motocrawler_item


#  main driver
if __name__ == "__main__":
    #  run scraper
    process = CrawlerProcess()
    process.crawl(SprzedajemyScraper)
    process.start()
