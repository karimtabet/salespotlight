#!/usr/bin/env python
import sys
from multiprocessing import Pool

from spiders import newlook, topshop
from mq import produce

SPIDERS = ['newlook', 'topshop']


def scrape_and_produce(spider):
    '''
    Uses the string spider parameter to get the actual spider module
    Calls mq.produce() with the generated data from the scrape
    '''
    spider = getattr(sys.modules[__name__], spider)
    for item in spider.scrape():
        produce(item)


def run():
    '''
    Use a multithreaded pool to call the scrape_and_produce function
    passing in a list of all spiders.
    It's necessary to send the string name of the spider module for
    multiprocessing to be happy.
    '''
    pool = Pool(8)
    pool.map(scrape_and_produce, SPIDERS)


if __name__ == '__main__':
    run()
