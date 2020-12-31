from celery import Celery

from scrapy.crawler import CrawlerProcess

from MotoCrawler.MotoCrawler.spiders import autoscout, mobile_de, olx, sprzedajemy

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task(bind=True, name="run_spiders")
def run_spiders():
    process = CrawlerProcess()
    process.crawl(autoscout.AutoScoutScraper)
    process.crawl(mobile_de.MobileDeScraper)
    process.crawl(olx.OlxScraper)
    process.crawl(sprzedajemy.SprzedajemyScraper)
    process.start()
