import os
# Python one-liner script, fires all spiders one-by-one.
# Alternative solution to Scrapy crawlall, which doesn't seem to work.
commands = [
    'scrapy crawl autoscout',
    'scrapy crawl mobile_de',
    'scrapy crawl olx',
    'scrapy crawl sprzedajemy'
]

if __name__ == "__main__":
    for com in commands:
        os.system(com)
