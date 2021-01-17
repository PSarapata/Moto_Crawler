Spiders
=======
This module hosts logic responsible for data collection in MotoCrawler. Four custom crawlers, based on Scrapy's
Spider class crawl different websites in search of car offers, based on json input file with specified brand/model
key-values.

This section will give you an overview on what a single spider does - there are only minor differences between each
spider's operating principles.

Input
------
First, let's take a look at how a model input file (consumed by spiders) should look like:

.. code-block:: json

    [
      {
        "brand": "Mitsubishi",
        "model": "Eclipse"
      },
      {
        "brand": "Mitsubishi",
        "model": "3000-GT"
      },
      {
        "brand": "Mazda",
        "model": "MX-5"
      }
    ]

Simple list of brand/model dictionary objects.

Output (optional)
-----------------
If filename references in a spider is uncommented, data could be stored locally in a .json file. The result would be
a list of objects similar to the one below:

.. code-block:: json

    {
        "id": "62335682",
        "url": "https://sprzedajemy.pl/mitsubishi-eclipse-2006r-paniowki-2-6bea9f-nr62335682",
        "brand": "Mitsubishi",
        "model": "Eclipse",
        "title": "Mitsubishi Eclipse 2006r.",
        "city": "Pani\u00f3wki",
        "voivodship": "\u015bl\u0105skie",
        "price": "22 990 z\u0142",
        "contact_seller": "PHONE_NUMBER_HERE",
        "image_urls": [
            "https://thumbs.img-sprzedajemy.pl/1000x901c/c0/24/d4/mitsubishi-eclipse-2006r-paniowki-533175890.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/00/d2/68/mitsubishi-eclipse-2006r-elektrochrom-lusterko-wst-paniowki-533175891.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/c9/36/21/mitsubishi-eclipse-2006r-eclipse-533175892.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/92/46/ae/mitsubishi-eclipse-2006r-lakier-metallic-paniowki-sprzedam-533175893.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/8f/d6/57/mitsubishi-eclipse-2006r-esp-eclipse-slaskie-paniowki-533175894.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/32/30/d1/mitsubishi-eclipse-2006r-benzyna-paniowki-sprzedam-533175895.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/00/6d/37/mitsubishi-eclipse-2006r-szyberdach-paniowki-sprzedam-533175896.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/49/55/67/mitsubishi-eclipse-2006r-533175897.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/3d/05/47/mitsubishi-eclipse-2006r-paniowki-533175898.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/f0/5d/97/mitsubishi-eclipse-2006r-paniowki-sprzedam-533175899.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/8e/e2/91/mitsubishi-eclipse-2006r-zarejestrowany-w-polsce-slaskie-paniowki-533175900.jpg",
            "https://thumbs.img-sprzedajemy.pl/1000x901c/07/8c/4e/mitsubishi-eclipse-2006r-benzyna-paniowki-533175901.jpg"
        ],
        "full_description": "MITSUBISHI ECLIPSE 2006r.\nSprowadzony do Polski w 2011r.\nW Kraju 2 w\u0142a\u015bciciel.\nLicznik podany w MILACH 66 993 w przybli\u017ceniu na 108ty\u015b. KM\nSamoch\u00f3d w dobrym stanie technicznym oraz wizualnym.\nMo\u017cliwo\u015b\u0107 kompleksowego sprawdzenia samochodu przed zakupem.\n\nPrzyjmujemy samochody w rozliczeniu.\n\nOferujemy zakupu auta bez wychodzenia z domu,\nZ dostaw\u0105 pod wskazany adres.\n\nAtrakcyjna oferta finansowania z kredytem 5% taniej.\nMo\u017cliwo\u015b\u0107 za\u0142atwienia wszystkich formalno\u015bci na miejscu, podczas jednej wizyty !!!\n\nKupuj\u0105cy zwolniony z op\u0142aty skarbowej.\n\nZapraszamy.\n\n439/20",
        "extra_info": [
            "klimatyzacja",
            "sk\u00f3rzana tapicerka",
            "centralny zamek",
            "elektryczne szyby",
            "wspomaganie kierownicy",
            "ABS",
            "ESP",
            "poduszka powietrzna",
            "szyberdach",
            "elektryczne lusterka",
            "aluminiowe felgi",
            "podgrzewane fotele",
            "radio",
            "immobilizer",
            "lakier metallic",
            "ASR (kontrola trakcji)",
            "CD",
            "elektrochrom. lusterko wst.",
            "isofix",
            "zmieniarka CD",
            "mo\u017cliwa zamiana",
            "Zarejestrowany w Polsce"
        ],
        "manufacturing_year": "2006",
        "mileage": "108000",
        "engine_capacity": "3828",
        "power": "263",
        "gearbox": "manualna"
    }

Spiders
---------

Let's have a closer look at what a spider actually does.

base parameters
^^^^^^^^^^^^^^^
.. code-block:: python

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

This is how you initate Spider class' attributes. Spider name and base URL should be self-explanatory. Pass in
any additional data to params if you wish to narrow down your search. Simply paste them to a URL in one of the
following class methods, as you would in a browser.

.. code-block:: python

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

The above is particularly important due to security reasons (and is considered good taste, you don't want to overload
the website!). First, identify yourself using headers and referer. Second, use custom download settings to limit the
rate at which you hit the website for data. **DO NOT** make it too short, or you **WILL GET BANNED**. Trust me. This
may even have legal consequences, so just don't.

init
^^^^
.. code-block:: python

        #  current offset
        current_offset = 0

        #  car (brand, model) tuple list
        cars = []
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

This block of code initiates the offset (pagination) and cars list, then reads the input json dictionary (see
`Input`_ section above), then saves it in the mentioned cars list.

start_requests
^^^^^^^^^^^^^^
.. code-block:: python

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

As per docstring information. Should you choose to receive a different `Output (optional)`_ format, uncomment
filename references.

parse_links
^^^^^^^^^^^
.. code-block:: python

        #  parse car links
        def parse_links(self, res):
            """
            Extracts url of all listed offers, including pagination, calls in parse_listing on each offer URL.

            :return: yields url for the offer and calls parse_listing method.

            """


parse_listing
^^^^^^^^^^^^^

.. code-block:: python

        #  parse car listings
        def parse_listing(self, res):
            """
            Extracts information from listing (offer) details.
            On success, yields a Scrapy MotoCrawlerItem instance,
            which is then processed by the DatabasePipeline.

            :return: custom Scrapy MotoCrawlerItem which is then fed into DatabasePipeline

            """

return
^^^^^^
Spiders allow two output formats, they either produce (**yield**) a custom Scrapy item, called MotoCrawlerItem, or
write scraped offer data to a locally stored .json file. Simply uncomment the lines to use the latter. (I would also
recommend commenting out the yield).

If you are interested in what happens with MotoCrawlerItem afterwards, have a read through :ref:`project-root`
section (Pipelines).

Run.py
-------
run.py is an inconspicuous python script sitting in **spiders/** module. It is actually a python one liner to fire
off all spiders one-by-one. Simply *open your terminal in spiders/ directory* and execute:

.. code-block:: bash

    python run.py
