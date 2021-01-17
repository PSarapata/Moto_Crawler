.. _project-root:

Project Root
============

This is the lower-most MotoCrawler/ directory. It is, in fact, the root of Scrapy project. You will find here:

::

    MotoCrawler
    ├── api/
    ├── authentication/
    ├── commands/
    ├── core/
    ├── docs/
    ├── spiders/
    |
    ├── __init__.py
    ├── items.py
    ├── manage.py
    ├── middlewares.py
    ├── pipelines.py
    ├── pytest.ini
    ├── settings.py
    └── setup.py

Modules have already been covered in other sections of this Documentation. __init__ is an empty file used by python
for better import management, and will not be covered.

Items.py
--------
Items file is a host to Scrapy's Item objects, which are very similar to Django's models and in fact, are mapped onto
instances of those items, by `Pipelines.py`_

Manage.py
---------
Django's default manager. `Documentation here <https://docs.djangoproject.com/en/3.1/ref/django-admin/>`_

Middlewares.py
--------------
Scrapy's middlewares. Those are stock, hence will not be covered here. If you seek knowledge, have a look in `Scrapy
official documentation <https://docs.scrapy.org/en/latest/index.html>`_

Pipelines.py
------------
This piece of code is responsible for mapping Scrapy Items onto Database items.

.. code-block:: python

        class DatabasePipeline(object):
            """Scrapy custom pipeline, manages spider-database data flow."""
            def process_item(self, item, spider):
                """Checks whether the Scrapy item produced by spider already exists in database.
                If it exists - skips and moves on to process another.
                If item does not exist - maps Scrapy item onto Django Offer, Photo and OfferPhoto
                models and saves new instances in the database."""
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

Pytest.ini
----------
Pytest configuration file.
Lets pytest find and apply django's settings.
python_files is used to allow pytest to correctly identify test files. As long as you follow naming convention, your
tests, you should get the expected behaviour.

Settings.py
-----------
Scrapy settings.
I recommend you to have a read through `Scrapy Settings documentation <https://docs.scrapy
.org/en/latest/topics/settings.html>`_. Meanwhile, let's take a closer look at one important step which integrates
Scrapy to work hand in hand with Django:

.. code-block:: python

    # Django integration
    import os
    import sys
    import django

    sys.path.append('ABSOLUTE_PATH_TO_YOUR_SETTINGS_PARENT_DIRECTORY')  # replace string with an actual path

    os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

    django.setup()

Setup.py
--------
*Currently not being used, the purpose of this file was to register custom "Scrapy crawlall" command, which would
fire all spiders with a one-liner, from any directory. Unfortunately, not only the command does not work, but
also overwrites Scrapy's defaults, rendering it useless.*
