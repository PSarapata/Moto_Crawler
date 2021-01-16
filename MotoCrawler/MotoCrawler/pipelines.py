# import psycopg2

from api.models import Offer, Photo, OfferPhoto
# from core.helpers.test_connect import hostname, username, password, database


class DatabasePipeline(object):
    """Scrapy custom pipeline, manages spider-database data flow."""
    # pass
    # def open_spider(self, spider):
    #     self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    #     self.cur = self.connection.cursor()
    #
    # def close_spider(self, spider):
    #     self.cur.close()
    #     self.connection.close()

    def process_item(self, item, spider):
        """Checks whether the Scrapy item produced by spider already exists in database.
        If it exists - skips and moves on to process another.
        If item does not exist - maps Scrapy item onto Django Offer, Photo and OfferPhoto
        models and saves new instances in the database."""
        # psycopg2 and raw SQL approach
        # self.cur.execute("""INSERT INTO API_OFFER(URL, BRAND, MODEL, TITLE, PRICE, DESCRIPTION) VALUES(%s, %s, %s, %s,
        # %s, %s);""", (item['url'], item['brand'], item['model'], item['title'], item['price'], item['description']))
        # for photo_url in item['photos']:
        #     self.cur.execute(f"""INSERT INTO API_PHOTO(URL) VALUE({photo_url});""")
        # self.connection.commit()
        # return item

        # Django ORM approach

        # Basic duplicates filter:
        try:
            offer = Offer.objects.get(url=item["url"])
            print("Offer already exists")
            return item
        except Offer.DoesNotExist:
            pass

        offer = Offer()
        offer.url = item["url"]
        offer.brand = item["brand"]
        offer.model = item["model"]
        offer.title = item["title"]
        offer.price = item["price"]
        offer.description = item["description"]
        offer.save()
        for photo_url in item["photos"]:
            photo = Photo()
            photo.url = photo_url
            photo.save()
            offerphoto = OfferPhoto.objects.create(offer=offer, photo=photo)
        return item
