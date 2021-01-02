import os

commands = [
    'scrapy crawl autoscout',
    'scrapy crawl mobile_de',
    'scrapy crawl olx',
    'scrapy crawl sprzedajemy'
]

if __name__ == "__main__":
    for com in commands:
        os.system(com)
