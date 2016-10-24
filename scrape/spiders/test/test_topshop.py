'''
Tests for the Topshop scraper
Uses test html pages copied from the Topshop website
'''
from os.path import join, dirname, realpath

from scrape.spiders.topshop import (get_sale_page_url,
                                    get_product_list_urls,
                                    get_product_urls,
                                    get_product_data)

FAKE_PRODUCT_LIST_PAGE_PATH = join(
    dirname(realpath(__file__)),
    'test_data',
    'topshop_product_list.html'
)
with open(FAKE_PRODUCT_LIST_PAGE_PATH) as page:
    FAKE_PRODUCT_LIST_PAGE = page.read()

FAKE_PRODUCT_PAGE_PATH = join(
    dirname(realpath(__file__)),
    'test_data',
    'topshop_product.html'
)
with open(FAKE_PRODUCT_PAGE_PATH) as page:
    FAKE_PRODUCT_PAGE = page.read()

def test_get_sale_page_url():
    '''
    Test get_sale_page_url function returns url to sale page
    '''
    got_url = get_sale_page_url(FAKE_PRODUCT_LIST_PAGE)
    expected_url = ('http://www.topshop.com/en/tsuk/category/'
                    'sale-offers-4181277')
    assert got_url == expected_url, 'expected %s but was %s' % (
        expected_url, got_url)

def test_get_product_list_urls():
    '''
    Test get_product_list_urls function returns tuple of links w/ category
    The common_set typecasts to set to union the two lists and deduplicate
    '''
    test_against = set([
        ('dresses', 'http://www.topshop.com/en/tsuk/category/'
                    'sale-offers-4181277/dresses/'
                    'N-8dvZqn9Zdgl?Nrpp=20&siteId=%2F12556'),
        ('tops', 'http://www.topshop.com/en/tsuk/category/'
                 'sale-offers-4181277/tops/'
                 'N-8dvZqnvZdgl?Nrpp=20&siteId=%2F12556'),
        ('jackets', 'http://www.topshop.com/en/tsuk/category/'
                    'sale-offers-4181277/jackets/'
                    'N-8dvZ1zcoZdgl?Nrpp=20&siteId=%2F12556'),
        ('jeans', 'http://www.topshop.com/en/tsuk/category/'
                  'sale-offers-4181277/jeans/'
                  'N-8dvZqnhZdgl?Nrpp=20&siteId=%2F12556')
    ])
    common_set = test_against & set(
        get_product_list_urls(FAKE_PRODUCT_LIST_PAGE))
    assert test_against == common_set, 'missing %s' % (
        test_against - common_set)

def test_get_product_urls():
    '''
    Test get_product_urls returns list of product page urls
    The common_set typecasts to set to union the two lists and deduplicate
    The test only checks the first 4 urls
    '''
    test_against = set([
        'http://www.topshop.com/en/tsuk/product/sale-offers-4181277/'
        'cupro-bomber-jacket-5816362?bi=0&ps=20',
        'http://www.topshop.com/en/tsuk/product/sale-offers-4181277/'
        'mesh-vest-dress-5512732?bi=0&ps=20',
        'http://www.topshop.com/en/tsuk/product/sale-offers-4181277/'
        'camo-print-wide-leg-trousers-5665644?bi=0&ps=20'
    ])
    common_set = test_against & set(
        get_product_urls(FAKE_PRODUCT_LIST_PAGE))
    assert test_against == common_set, 'missing %s' % (
        test_against - common_set)

def test_get_product_title():
    '''
    Test get_product_data returns correct title
    '''
    assert (
        get_product_data(FAKE_PRODUCT_PAGE)['title'] ==
        'Cupro Bomber Jacket'
    )

def test_get_product_image_url():
    '''
    Test get_product_data returns correct image url
    '''
    got_url = get_product_data(FAKE_PRODUCT_PAGE)['image_url']
    expected_url = ('http://media.topshop.com/wcsstore/TopShop/images/'
                    'catalog/TS04Z03KOLV_Large_F_1.jpg')
    assert expected_url == got_url, 'expected %s but was %s' % (
        expected_url, got_url)

def test_get_product_rrp():
    '''
    Test get_product_data returns correct rrp
    '''
    got_rrp = get_product_data(FAKE_PRODUCT_PAGE)['rrp']
    expected_rrp = 49.00
    assert expected_rrp == got_rrp, 'expected %s but was %s' % (
        expected_rrp, got_rrp)

def test_get_product_sale_price():
    '''
    Test get_product_data returns correct sale price
    '''
    got_price = get_product_data(FAKE_PRODUCT_PAGE)['sale_price']
    expected_price = 25.00
    assert expected_price == got_price, 'expected %s but was %s' % (
        expected_price, got_price)

def test_get_product_sku():
    '''
    Test get_product_data returns correct sku
    '''
    got_sku = get_product_data(FAKE_PRODUCT_PAGE)['sku']
    expected_sku = 'TS04Z03KOLV'
    assert expected_sku == got_sku, 'expected %s but was %s' % (
        expected_sku, got_sku)
