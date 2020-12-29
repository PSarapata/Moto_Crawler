# Moto_Crawler
My CodersLab final project, car selling websites web scraper built with Scrapy and Celery.


16.12.2020 10:00
----------------
Pushed first stage of my project. As per commit message, I read Scrapy documentation first, then found a nice commercial web scraping project example (real estate)
and based my first Spider on this code. Currently this spider feeds on input.json file, reads through the brand/model dictionary items and scrapes the car selling
website for offers. It then creates an output .json file with each car details.

@update:
---------------
Second Spider crawls another website, which consists of own and external offers. There is a small bug with extracting two feature keys. Will continue working on this after REST API workshop.

20.12.2020 21:00
---------------
Current functionality: Start each spider manually from console. Spiders scrape through 4 popular car selling websites based on input json file, return ready-to-process dictionary items in a json output file. I plan to add one more spider, add pagination for all, then move on to handle PostgreSQL database.

29.12.2020 14:30
---------------
I am currently watching tutorials to expand my knowledge on Django REST framework and API building. I might potentially build a full-stack app with a simple React front-end. After I've finished with this, I will move on to Celery tutorials and then hopefully add some code again. Apologies for being quiet. :)
