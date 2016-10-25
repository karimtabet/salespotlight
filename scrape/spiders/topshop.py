#!/usr/bin/env python
'''Module to scrape Newlook website'''

import re
import json
from logging import getLogger

import requests
from bs4 import BeautifulSoup

# from couchdb_handler import add_product_to_db

LOG = getLogger(__name__)

ROOT_URL = 'http://www.topshop.com'


def get_product_data(html):
    '''Return a dict of product data from product page'''
    soup = BeautifulSoup(html, 'lxml')

    # get an HTML script element containing a dict of product details
    script = (soup.find('script',
                        text=re.compile('window.universal_variable'))
              .get_text().strip())
    product_json = json.loads(script[28:])

    scraped_cat = product_json['product']['category']
    categories = []
    if 'Sale' not in scraped_cat and len(scraped_cat) > 2:
        categories = [product_json['product']['category']]

    return {
        'title': product_json['product']['name'],
        'categories': categories,
        'rrp': float(product_json['product']['unit_price']),
        'sale_price': float(product_json['product']['unit_sale_price']),
        'sku': product_json['product']['sku_code'],
        'image_url': product_json['product']['image_url']
    }


def get_product_urls(html):
    '''Return list of product urls'''
    soup = BeautifulSoup(html, 'lxml')
    page_urls = [a.attrs.get('href') for a in
                 soup.select('a[class*=product_action]')]
    if page_urls:
        return page_urls


# def add_products_to_db(product_list_url):
#     '''Add products to DB from a URL containing a list of products'''
#     try:
#         product_urls = get_product_page_urls(product_list_url)
#     except TypeError:
#         return
#     if product_urls:
#         for url in product_urls:
#             try:
#                 add_product_to_db(get_product_data(url))
#             except AttributeError:
#                 pass


def get_sale_page_url(html):
    '''
    Get the sale page url from Topshop html
    '''
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('a', title='Sale & Offers').get('href')


def get_product_list_urls(html):
    '''
    Return a tuple of category name and url of a product list page
    '''
    soup = BeautifulSoup(html, 'lxml')
    return [(a.attrs.get('title'), ROOT_URL + a.attrs.get('href')) for a in
            soup.select('div[class*=ce3_product_type] a')]

def scrape():
    '''Scrape entire site'''
    LOG.info('Scraping Topshop products')
    products_response = []
    response = requests.get(ROOT_URL)
    sale_page_url = get_sale_page_url(response.text)
    sale_page = requests.get(sale_page_url).text
    product_list_urls = get_product_list_urls(sale_page)
    for category, list_url in product_list_urls:
        product_list_page = requests.get(list_url).text
        product_urls = get_product_urls(product_list_page)
        for product_url in product_urls:
            product_page = requests.get(product_url).text
            product_data = get_product_data(product_page)
            product_data['url'] = product_url
            product_data['categories'].append(category)
            products_response.append(product_data)
            yield product_data

if __name__ == '__main__':
    scrape()
