#!/usr/bin/env python3.5
'''Module to scrape Newlook website'''

import re
import yaml
import sys
from multiprocessing import Pool
from logging import getLogger

import requests
from bs4 import BeautifulSoup

# from couchdb_handler import add_product_to_db

LOG = getLogger(__name__)

ROOT_URL = 'http://www.newlook.com'

# with open('category_map.yml', 'r') as stream:
#     try:
#         CATEGORY_MAP = yaml.load(stream)
#     except yaml.YAMLError as error:
#         LOG.error('failed to parse category map yaml with error: {e}',
#                   e=error)
#         sys.exit()


def get_sale_urls(html):
    '''Return list of urls of pages that list products on sale'''
    soup = BeautifulSoup(html, 'lxml')
    sale_urls = soup.findAll('a', {'href': re.compile('/shop/sale.*')})
    return [(url.text, url.get('href')) for url in sale_urls
            if ROOT_URL in url.get('href')]


def get_product_urls(html):
    '''Return list of product urls'''
    soup = BeautifulSoup(html, 'lxml')
    urls = [ROOT_URL + a.attrs.get('href') for a in
            soup.select('li.product a[href*=/shop/]')]
    return list(set(urls))  # Set used to deduplicate


# def add_products_to_db(product_list_url):
#     '''Add products to DB from list of product urls'''
#     for product_url in get_product_page_urls(product_list_url):
#         add_product_to_db(get_product_data(product_url))


def get_product_data(html):
    '''Return a dict of product data from product page'''
    soup = BeautifulSoup(html, 'lxml')
    meta_content = (
        soup.find('meta', {'name': 'keywords'})
        .attrs.get('content').split(',')
    )
    product_data = {}
    product_data['title'] = meta_content[0]

    # for parent_cat, child_cats in CATEGORY_MAP['mens'].items():
    #     category_split = [word for word in category.lower().split()]
    #     for child_cat in child_cats:
    #         if any(word in child_cat for word in category_split):
    #             print(child_cat)
    #             print(parent_cat)

    try:
        product_data['rrp'] = float(re.findall(
            r'\d+\.\d+', soup.select('.price .wasPrice')[0].get_text())[0])
    except IndexError:
        product_data['rrp'] = float(re.findall(
            r'\d+\.\d+', soup.select('.price .productPrice')[0].get_text())[0])
    try:
        product_data['sale_price'] = float(re.findall(
            r'\d+\.\d+', soup.select('.price .salePrice')[0].get_text())[0])
    except IndexError:
        pass
    product_data['sku'] = soup.select('.product-code span')[0].get_text()
    product_data['description'] = (soup.select('.information-section p')[0]
                                   .get_text())
    small_image_url = (soup.select('.product-zoom-gallery img')[0].attrs
                       .get('src').replace('//', 'http://'))
    product_data['image_url'] = small_image_url[:small_image_url.find('?')]
    return product_data


def scrape():
    '''Scrape entire site'''
    LOG.info('Scraping Newlook products')
    products_response = []
    first_page = ROOT_URL + '/index.html'
    response = requests.get(first_page, allow_redirects=False)
    sale_urls = get_sale_urls(response.text)
    for category, sale_url in sale_urls:
        if 'View All' not in category:
            product_urls = get_product_urls(requests.get(sale_url).text)
            for product_url in product_urls:
                html = requests.get(product_url).text
                product_data = get_product_data(html)
                product_data['url'] = product_url
                product_data['categories'] = [category]
                products_response.append(product_data)
                yield product_data


    # soup = BeautifulSoup(response.text, 'lxml')
    # product_list_urls = [a.attrs.get('href') for a in
    #                      soup.select('a[href*=/shop/sale]')]
    # sale_links = soup.findAll('a', {'href' : re.compile('/shop/sale.*')})
    # print([link.text for link in sale_links])
    # pool = Pool(8)
    # pool.map(add_products_to_db, product_list_urls)


if __name__ == '__main__':
    scrape()
