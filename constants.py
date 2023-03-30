"""
This file contains all constants used in our webscraping project. Files that call it are
all-recipe-web-scraper.py, command_line.py, and scrape_links.py.
"""

# Scraping constants
SOURCE = "https://www.allrecipes.com/recipes-a-z-6735880"
INDEX_LINK_CLASS = 'link-list__link'
TOP_LINK_CLASS = 'comp card--image-top mntl-card-list-items mntl-document-card mntl-card card card--no-image'
BOTTOM_LINK_CLASS = 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image'
INGREDIENTS_CLASS = 'mntl-structured-ingredients__list'
DETAILS_CONTENT = 'mntl-recipe-details__content'
DETAILS_LABEL = 'mntl-recipe-details__label'
DETAILS_VALUE = "mntl-recipe-details__value"
REVIEWS_CLASS = 'mntl-recipe-review-bar__comment-count_1-0'
RATING_CLASS = 'mntl-recipe-review-bar__rating_1-0'
NUTRITION_CLASS = 'mntl-nutrition-facts-summary__table'
DATE_CLASS = 'mntl-attribution__item-date'
CATEGORY_CLASS = 'mntl-breadcrumbs'
INSTRUCTIONS_CLASS = 'comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup'

# Other constants
NO_REVIEWS = "0"
TIME = "Time"
AMOUNT_INDEX = 0
LABEL_INDEX = 1
GRAMS_INDEX = -1
GRAMS = 'g'
SERVINGS = 'Servings:'
NEXT_INDEX = 1
NEXT_PAIR = 2
MIN_ARGS = 1
MAX_ARGS = 11
PUBLISHED_ON = 2
HOURS = 24
MINS = 60
