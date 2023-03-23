"""
This .py file scrapes the allrecipes website using python's beautiful soup, requests, and regex libraries for
various data points. The parameters we are collecting are Recipe Title, Ingredients, recipe details (Prep Time,
Cook Time, etc.), Number of Reviews, Recipe Rating, Nutrition Facts, Date published, and
Recipe Category (e.g. Main Dish, Breakfast).
"""
# import libraries
from bs4 import BeautifulSoup
import requests
import re
import logging
import argparse
import sys

SOURCE = "https://www.allrecipes.com/recipes-a-z-6735880"


def get_index_links(main_index_link):  # ADDED INDEX FOR TESTS !!!!! Remove to start data mining !!!!!!!
    """
    Receives the source url and pulls the highest level urls from the index page.
    :param: str: url
    :return: list: urls
    """
    response = requests.get(main_index_link).text
    soup = BeautifulSoup(response, features="html.parser")
    a_tags = soup.find_all('a', class_='link-list__link')
    index_links = [a_tag['href'] for a_tag in a_tags]
    return index_links[0:2]


def get_recipe_links(index_link):
    """
    Receives a link from the index_links and scrapes all the recipe urls from that page.
    :param: str: url
    :return: list: urls
    """
    response = requests.get(index_link).text
    soup = BeautifulSoup(response, features="html.parser")
    top_link_tags = soup.find_all('a', {
        'class': 'comp card--image-top mntl-card-list-items mntl-document-card mntl-card card card--no-image'})
    top_links = [attr['href'] for attr in top_link_tags]
    bottom_link_tags = soup.find_all('a', class_='comp mntl-card-list-items mntl-document-card mntl-card card '
                                                 'card--no-image')
    bottom_links = [attr['href'] for attr in bottom_link_tags]
    recipe_links = top_links + bottom_links
    return recipe_links


def get_all_links(index_links):
    """
    Receives a list of the urls from the index page and calls the get_recipe function on each of them
    to scrape the recipe urls from all pages. Returns a list of all recipe links.
    :param: list: index links
    :return: list: urls
    """
    all_links = []
    for link in index_links:
        all_links.extend(get_recipe_links(link))
        logging.info(f'Links from: {link}  retrieved')
    return all_links


def make_soup(link):  # func name changed to avoid confusion with argparse
    """
    This function will provide the BeautifulSoup object for the scraping functions called on each recipe link.
    :param: str: link str
    :return: BeautifulSoup object
    """
    response = requests.get(link).text
    soup = BeautifulSoup(response, features="html.parser")
    return soup


def get_title(soup):
    """
    Scrapes the title from each recipe page.
    :param: BeautifulSoup object
    :return: str: recipe title
    """
    title = soup.title.string
    return title


def get_ingredients(soup):
    """
    Scrapes the ingredients, returns a list of strings with each ingredient and its quantity. To filter out
    non-recipe web pages, if there are no ingredients listed, will just return an empty list.
    :param: BeautifulSoup object
    :return: list: ingredients
    """
    ingredients = []
    p_tags = soup.find_all("ul", class_="mntl-structured-ingredients__list")
    for p in p_tags:
        ingredients.append(p.text.strip())
    if len(ingredients) == 0:
        return ingredients
    ingredients = ''.join(ingredients).replace('\n\n\n', ' ?').split('?')
    return ingredients


def get_recipe_details(soup):
    """
    Scrapes the recipe details (e.g., "Prep Time", "Cook Time", etc.) and returns then as a dictionary.
    :param: BeautifulSoup object
    :return: dict: recipe_details
    """
    grid_elements = soup.find('div', class_='mntl-recipe-details__content').find_all('div',
                                                                                     class_='mntl-recipe-details__label')
    recipe_details = {}
    for element in grid_elements:
        label = element.text.strip()
        data = element.find_next_sibling(class_="mntl-recipe-details__value").text.strip()
        recipe_details[label] = data
    return recipe_details


def get_num_reviews(soup):
    """
    Returns the number of reviews on each recipe as an integer.
    :param: BeautifulSoup object
    :return: str: number of reviews
    """
    num_reviews_elem = soup.find('div', {'id': 'mntl-recipe-review-bar__comment-count_1-0'}).text
    if any(char.isdigit() for char in num_reviews_elem):
        num_reviews = "".join([i for i in num_reviews_elem if i.isnumeric()])
    else:
        num_reviews = "0"  # should we make this a global constant?
    return num_reviews


def get_rating(soup):
    """
    Returns the rating of the recipe as a float. If there are no reviews on the recipe, will
    return the rating as NoneType object.
    :param: BeautifulSoup object
    :return: float: recipe rating or None
    """
    rating_elem = soup.find('div', {'id': 'mntl-recipe-review-bar__rating_1-0'})
    if rating_elem:
        rating_elem_text = rating_elem.text.strip()
        rating = float(re.search(r'\d+.\d+', rating_elem_text).group())
    else:
        rating = None
    return rating


def get_nutrition_facts(soup):
    """
    Extracts nutrition facts for each recipe and stores then in a dictionary.
    :param: BeautifulSoup object
    :return: dict: nutrition facts
    """
    nutrition_table = soup.find('table', class_='mntl-nutrition-facts-summary__table')
    nutrition_facts = {}
    for row in nutrition_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 2:
            key = cells[0].text.strip().lower()
            value = cells[1].text.strip()
            nutrition_facts[value] = key
    return nutrition_facts


def get_date_published(soup):
    """
    Extracts the date that the recipe was published on allrecipes.com
    :param: BeautifulSoup object
    :return: str: date published
    """
    date_elem = soup.find('div', class_='mntl-attribution__item-date')
    date_published = date_elem.text.strip().replace('Updated on ', '').split()
    date_published = " ".join(date_published[2:])
    return date_published


def get_categories(soup):
    """
    Gets the categories of the recipe (e.g. breakfast, main dish, vegan) and returns them as a list of strings.
    :param: BeautifulSoup object
    :return: list: categories
    """
    breadcrumb = soup.find('ul', class_='mntl-breadcrumbs')
    categories = [elem.text.strip() for elem in breadcrumb.find_all('li')]
    return categories


# For the --all argument: function to check if any other arguments are provided
def has_other_args(args):
    """
    Check if any other argument is provided alongside the 'all' flag.
    :param args: argparse.Namespace object containing the arguments
    :return: bool: True if any other argument is provided, False otherwise
    """
    return any([args.title, args.ingredients, args.details, args.reviews, args.rating, args.nutrition,
                args.published, args.category])


def main():
    """
    Takes in the index link for allrecipes.com to begin scraping the site. Iterates over
    all recipe links and calls scraping functions on each of them. Iteration will skip over non-recipe web pages.
    :return: None: writes output to scraping.log file
    """

    # Set up logging configuration
    logging.basicConfig(
        filename='logging_info.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    index_links = get_index_links(SOURCE)
    all_links = get_all_links(index_links)

    # Set argparse arguments
    parser = argparse.ArgumentParser(description='Scrape data from allrecipes.com')
    parser.add_argument('--title', action='store_true', help='Scrape recipe title')
    parser.add_argument('--ingredients', action='store_true', help='Scrape recipe ingredients')
    parser.add_argument('--details', action='store_true', help='Scrape recipe details (prep time, cook time, etc.)')
    parser.add_argument('--reviews', action='store_true', help='Scrape number of reviews')
    parser.add_argument('--rating', action='store_true', help='Scrape recipe rating')
    parser.add_argument('--nutrition', action='store_true', help='Scrape nutrition facts')
    parser.add_argument('--published', action='store_true', help='Scrape publish date')
    parser.add_argument('--category', action='store_true', help='Scrape recipe category')
    parser.add_argument('--all', action='store_true', help='Scrape all available data')

    # Use parse_known_args() instead of parse_args()
    args, unknown_args = parser.parse_known_args()

    # Check if any arguments were passed
    if len(sys.argv) <= 1:
        parser.print_help()
        logging.info(f'No argument was passed')
        print('\nAt least one argument is required.')
        exit()

    # Check if too many arguments were passed
    elif len(sys.argv) > 9:
        parser.print_help()
        logging.info(f'Too many arguments')
        print('\ntoo many arguments were passed.')
        exit()

    # Check if unrecognized arguments were passed
    if unknown_args:
        parser.print_help()
        logging.info(f'Unrecognized arguments: {unknown_args}')
        print(f'\nUnrecognized arguments: {unknown_args}')
        exit()

    # Check if --all is provided with other arguments
    if args.all and has_other_args(args):
        parser.print_help()
        logging.info(f'--all argument should not be used with other arguments')
        print('\n--all argument should not be used with other arguments.')
        exit()

    # If user chooses to scrape all avaiable data
    if args.all:
        args.title = args.ingredients = args.details = args.reviews = args.rating = args.nutrition = args.published = args.category = True

    count = 1
    with open('scraping.log', 'w+') as output_file:
        for link in all_links:
            soup = make_soup(link)
            ingredients = get_ingredients(soup)

            # to avoid scraping web pages that aren't recipes
            if len(ingredients) == 0:
                continue

            # call each scraping method based on the argparse arguments
            scraped_data = {}
            if args.title:
                scraped_data['title'] = get_title(soup)
            if args.ingredients:
                scraped_data['ingredients'] = get_ingredients(soup)
            if args.details:
                scraped_data['details'] = get_recipe_details(soup)
            if args.reviews:
                scraped_data['reviews'] = get_num_reviews(soup)
            if args.rating:
                scraped_data['rating'] = get_rating(soup)
            if args.nutrition:
                scraped_data['nutrition'] = get_nutrition_facts(soup)
            if args.published:
                scraped_data['published'] = get_date_published(soup)
            if args.category:
                scraped_data['category'] = get_categories(soup)

            # write scraped data to output file
            output_file.write(f'\nRecipe {count}:\n')
            for key, value in scraped_data.items():
                output_file.write(f'{key.capitalize()}: {value}\n')
            output_file.write('\n')

            # logging info
            logging.info(f'Scraped recipe number: {count}\n')
            print(f'Scraping recipe number {count}...')
            count += 1


if __name__ == '__main__':
    main()
