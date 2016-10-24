'''
Tests for the Newlook scraper
Uses test html pages copied from the Newlook website
'''
from os.path import join, dirname, realpath

from scrape.spiders.newlook import (get_sale_urls,
                                    get_product_urls,
                                    get_product_data)


FAKE_PRODUCT_LIST_PAGE_PATH = join(
    dirname(realpath(__file__)),
    'test_data',
    'newlook_product_list.html'
)
with open(FAKE_PRODUCT_LIST_PAGE_PATH) as page:
    FAKE_PRODUCT_LIST_PAGE = page.read()

FAKE_PRODUCT_PAGE_PATH = join(
    dirname(realpath(__file__)),
    'test_data',
    'newlook_product.html'
)
with open(FAKE_PRODUCT_PAGE_PATH) as page:
    FAKE_PRODUCT_PAGE = page.read()


def test_get_sale_urls():
    '''
    Test get_sale_urls function returns tuple of links w/ category
    The common_set typecasts to set to union the two lists and deduplicate
    '''
    test_against = set([
        ('Tops', 'http://www.newlook.com/shop/sale/view-all-sale/'
                 'inspire-sale/tops/_/N-kx0Zeqf'),
        ('Heels', 'http://www.newlook.com/shop/sale/view-all-sale/'
                  'shoes-boots-sale/high-heel/_/N-kxuZ1z141vn'),
        ('Jewellery', 'http://www.newlook.com/shop/sale/view-all-sale/'
                      'accessories-sale/jewellery/_/N-kwfZetg'),
        ('Dresses', 'http://www.newlook.com/shop/sale/view-all-sale/'
                    'inspire-sale/dresses/_/N-kx0Zgkf')
    ])
    common_set = test_against & set(
        get_sale_urls(FAKE_PRODUCT_LIST_PAGE))
    assert test_against == common_set, 'missing %s' % (
        test_against - common_set)


def test_get_product_urls():
    '''
    Test get_product_urls returns list of product urls
    The common_set typecasts to set to union the two lists and deduplicate
    '''
    test_against = set([
        'http://www.newlook.com/shop/womens/'
        'petite/petite-cream-lace-up-bodysuit_379082014',
        'http://www.newlook.com/shop/womens/knitwear/'
        'burgundy-contrast-stripe-cropped-jumper-_381895267',
        'http://www.newlook.com/shop/womens/'
        'tops/white-colour-block-shoulder-panel-bodysuit-_382205219'
    ])
    common_set = test_against & set(
        get_product_urls(FAKE_PRODUCT_LIST_PAGE))
    assert test_against == common_set, 'missing %s' % (
        test_against - common_set)


def test_no_duplicates():
    '''
    Test get_product_page_urls does not return duplicates
    '''
    assert len(get_product_urls(FAKE_PRODUCT_LIST_PAGE)) == 96


def test_get_product_title():
    '''
    Test get_product_data returns correct title
    '''
    assert (
        get_product_data(FAKE_PRODUCT_PAGE)['title'] ==
        'Olive Green Fine Knit Cold Shoulder Top'
    )


def test_get_product_image_url():
    '''
    Test get_product_data returns correct image url
    '''
    assert (
        get_product_data(FAKE_PRODUCT_PAGE)['image_url'] ==
        'http://media.newlookassets.com/i/newlook/379985533/womens/tops/'
        't-shirts/olive-green-fine-knit-cold-shoulder-top/'
    )


def test_get_product_rrp():
    '''
    Test get_product_data returns correct rrp
    '''
    assert (
        get_product_data(FAKE_PRODUCT_PAGE)['rrp'] ==
        9.99
    )


def test_get_product_sale_price():
    '''
    Test get_product_data returns correct sale price
    '''
    assert (
        get_product_data(FAKE_PRODUCT_PAGE)['sale_price'] ==
        7.49
    )


def test_get_product_sku():
    '''
    Test get_product_data returns correct sku
    '''
    assert (
        get_product_data(FAKE_PRODUCT_PAGE)['sku'] ==
        '379985533'
    )
