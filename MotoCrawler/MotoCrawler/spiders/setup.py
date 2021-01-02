from setuptools import setup, find_packages

setup(name='scrapy-MotoCrawler',
      entry_points={
          'scrapy.commands': [
              'runall=MotoCrawler.commands:runall',
          ],
      },
      )
