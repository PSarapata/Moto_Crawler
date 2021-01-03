# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MotocrawlerItem(scrapy.Item):
    """Basic Offer class database item."""
    # pass
    url = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    photos = scrapy.Field()
