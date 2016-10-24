'''
Tests for the categoriser
'''
from classify.categorise import (get_parent_category,
                                 get_category_from_title,
                                 get_all_subcategories)


def test_get_parent_category():
    '''
    Test get_parent_category function returns correct parents
    '''
    parent_cat = get_parent_category('blouses', is_womens=True)
    assert parent_cat == 'tops', 'expected %s but was %s' % (
        'tops', parent_cat)


def test_get_category_from_title():
    '''
    Test get_category_from_title function can determine if a
    substring of a title contains one of our categories and
    extracts it
    '''
    extracted_cat = get_category_from_title('Brown Leather Coat')
    assert extracted_cat == 'coats', 'expected %s but was %s' % (
        'coats', extracted_cat)


def test_get_category_1_word_title():
    '''
    Test get_category_from_title function can extract a category
    from a title containing only one word.
    '''
    extracted_cat = get_category_from_title('Jacket')
    assert extracted_cat == 'jackets', 'expected %s but was %s' % (
        'jackets', extracted_cat)


def test_get_category_no_match():
    '''
    Test get_category_from_title function returns None
    when there is no match
    '''
    extracted_cat = get_category_from_title('Something Else')
    assert extracted_cat is None, 'expected %s but was %s' % (
        None, extracted_cat)


def test_get_all_subcategories():
    '''
    Test that get_all_subcategories function returns the correct
    amount of unique subcategories as per mappings.yml
    '''
    got_subcat_length = len(get_all_subcategories())
    assert got_subcat_length == 28, 'expected %s but was %s' % (
        28, got_subcat_length)
