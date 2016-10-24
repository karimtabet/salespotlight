import sys
from logging import getLogger
import yaml


LOG = getLogger(__name__)

with open('mappings.yml', 'r') as stream:
    try:
        MAPPINGS = yaml.load(stream)
    except yaml.YAMLError as error:
        LOG.error('failed to parse mappings yaml with error: {e}',
                  e=error)
        sys.exit()


def get_parent_category(category, is_womens):
    '''
    Get the parent category of an existing mens or womens category
    '''
    gender = 'womens' if is_womens else 'mens'
    for parent_cat, child_cats in MAPPINGS[gender].items():
        category_split = [word for word in category.lower().split()]
        for child_cat in child_cats:
            if any(word in child_cat for word in category_split):
                return parent_cat


def get_category_from_title(title):
    '''
    Return category if any substring of the title matches our
    set of categories.
    '''
    words = [word.lower() for word in title.split()]
    for word in words:
        for cat in get_all_subcategories():
            if word in cat:
                return cat


def get_all_subcategories():
    '''
    Flatten category mappings and return unique set of all
    subcategories.
    '''
    return list(set([
        cat for sublist in
        [sub for parent, sub in MAPPINGS['womens'].items()] +
        [sub for parent, sub in MAPPINGS['mens'].items()]
        for cat in sublist
    ]))
