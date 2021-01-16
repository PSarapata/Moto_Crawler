# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MotocrawlerItem(scrapy.Item):
    """Custom Scrapy item, built to resemble Offer Django api model,
    with additional photo field to hold relation. See pipelines.py
    file to see how Scrapy Items are being handled after creation."""

    url = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    photos = scrapy.Field()
