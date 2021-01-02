# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import psycopg2

from core.helpers.test_connect import hostname, username, password, database


class DatabasePipeline(object):
    # pass
    def open_spider(self, spider):
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("""INSERT INTO API_OFFER(URL, BRAND, MODEL, TITLE, PRICE, DESCRIPTION) VALUES(%s, %s, %s, %s,
        %s, %s)""", (item['url'], item['brand'], item['model'], item['title'], item['price'], item['description']))
        self.connection.commit()
        return item
