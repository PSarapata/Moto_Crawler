from celery import Celery

from scrapy.crawler import CrawlerProcess

from MotoCrawler.MotoCrawler.spiders import autoscout, mobile_de, olx, sprzedajemy


app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task(bind=True, name="run_spiders")
def run_spiders():
    """Currently not implemented. The idea behind this script
    was to use Celery to queue Scrapy crawlers. It is currently
    done manually in terminal, by typing 'python run.py'
    from /spiders module directory."""
    process = CrawlerProcess()
    process.crawl(autoscout.AutoScoutScraper)
    process.crawl(mobile_de.MobileDeScraper)
    process.crawl(olx.OlxScraper)
    process.crawl(sprzedajemy.SprzedajemyScraper)
    process.start()
