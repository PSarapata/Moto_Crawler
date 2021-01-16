# from scrapy.commands import ScrapyCommand
# from scrapy.crawler import CrawlerRunner
#
# from scrapy.utils.conf import arglist_to_dict
#
# from scrapy.exceptions import UsageError
# from scrapy.utils.project import get_project_settings
#
#
# THE GOAL HERE WAS TO CREATE A CUSTOM SCRAPY COMMAND TO RUN ALL SPIDERS IN PARALLEL,
# HOWEVER IT DOES NOT WORK. FURTHERMORE, IT ALSO FIDDLES WITH SCRAPY'S BASE FUNCTIONALITIES!
# I LEFT THE CODE HERE, SINCE AFTER SOME TWEAKING THERE IS A CHANCE IT MAY COME IN HANDY TO SOMEONE,
# BUT IT IS NOT USED IN THE PROJECT.
#
# class Command(ScrapyCommand):
#     requires_project = True
#
#     def syntax(self):
#         return '[options]'
#
#     def short_desc(self):
#         return 'Runs all of the spiders'
#
#     def add_options(self, parser):
#         ScrapyCommand.add_options(self, parser)
#         parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
#                           help="set spider argument (may be repeated)")
#         parser.add_option("-o", "--output", metavar="FILE",
#                           help="dump scraped items into FILE (use - for stdout)")
#         parser.add_option("-t", "--output-format", metavar="FORMAT",
#                           help="format to use for dumping items with -o")
#
#     def process_options(self, args, opts):
#         ScrapyCommand.process_options(self, args, opts)
#         try:
#             opts.spargs = arglist_to_dict(opts.spargs)
#         except ValueError:
#             raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
#
#     def run(self, args, opts):
#         settings = get_project_settings()
#
#         spider_loader = self.crawler_process.spider_loader
#         for spidername in args or spider_loader.list():
#             print("*********crawlall spidername************" + spidername)
#             self.crawler_process.crawl(spidername, **opts.spargs)
#
#         self.crawler_process.start()

# Second approach:

# import sys
# import os
#
# from twisted.internet import reactor, defer
# from scrapy import cmdline
# from scrapy.commands import ScrapyCommand
# from scrapy.crawler import CrawlerProcess
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from scrapy.exceptions import UsageError
# from scrapy.utils.conf import arglist_to_dict
# from scrapy.utils.python import without_none_values
# from scrapy.utils.log import configure_logging
#
#
# class Command(ScrapyCommand):
#     requires_project = True
#
#     def syntax(self):
#         return "<spider1 spider ,..> | all [options] "
#
#     def short_desc(self):
#         return "Run many spiders"
#
#     def add_options(self, parser):
#         ScrapyCommand.add_options(self, parser)
#         parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
#                           help="set spiders arguments (may be repeated)")
#         parser.add_option("-o", "--output", metavar="FILE",
#                           help="dump scraped items into FILE (use - for stdout)")
#         parser.add_option("-t", "--output-format", metavar="FORMAT",
#                           help="format to use for dumping items with -o")
#
#     def process_options(self, args, opts):
#         ScrapyCommand.process_options(self, args, opts)
#
#         try:
#             opts.spargs = arglist_to_dict(opts.spargs)
#         except ValueError:
#             raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
#
#         if not opts.spargs:
#             raise UsageError("You need pass a least one argument -a value, use -a NAME=VALUE", print_help=False)
#
#         if opts.output:
#             if opts.output == '-':
#                 self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
#             else:
#                 self.settings.set('FEED_URI', opts.output, priority='cmdline')
#             feed_exporters = without_none_values(self.settings.getwithbase('FEED_EXPORTERS'))
#             valid_output_formats = feed_exporters.keys()
#             if not opts.output_format:
#                 opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
#             if opts.output_format not in valid_output_formats:
#                 raise UsageError("Unrecognized output format '%s', set one"
#                                  " using the '-t' switch or as a file extension"
#                                  " from the supported list %s" % (opts.output_format,
#                                                                   tuple(valid_output_formats)))
#             self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')
#
#     def run(self, spiders_names, opts):
#         # crawler_process = CrawlerProcess(get_project_settings())
#         configure_logging()
#         crawler_runner = CrawlerRunner(get_project_settings())
#
#         if 'all' in spiders_names and len(spiders_names) > 1:
#             raise UsageError('You not use "all" with others spiders names, '
#                              'please chose "all" or a list of name', print_help=True)
#
#         if spiders_names[0] == 'all':
#             spiders_names = crawler_process.spider_loader.list()
#         elif len(spiders_names) > 0:
#             spiders_list = spiders_names
#
#         @defer.inlineCallbacks
#         def crawl():
#             for spiders_name in spiders_names:
#                 yield crawler_runner.crawl(spiders_name, **opts.spargs)
#             reactor.stop()
#
#         crawl()
#         reactor.run()

        # try:
        #     for spiders_name in spiders_names:
        #         crawler_process.crawl(spiders_name, **opts.spargs)
        # except KeyError:
        #     raise UsageError('Spider "{}" not found, please check the names passed in the args'.format(spiders_name))
        # except Exception as e:
        #     raise e

        # crawler_process.start()