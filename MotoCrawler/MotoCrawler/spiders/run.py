from scrapy import cmdline

cmdline.execute('scrapy crawl autoscout'.split())  # Add the command to run the crawler
cmdline.execute('scrapy crawl mobile_de'.split())
cmdline.execute('scrapy crawl olx'.split())
cmdline.execute('scrapy crawl sprzedajemy'.split())
