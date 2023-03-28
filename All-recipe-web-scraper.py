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


def get_index_links(main_index_link):  # ADDED INDEX FOR TESTS !!!! Remove to start data mining !!!!!!!
    """
    Receives the source url and pulls the highest level urls from the index page.
    :param: str: url
    :return: list: urls
    """
    msg = 'Error getting index links'
    response = get_exception(main_index_link, msg)
    if response:
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
    msg = 'Error getting recipe links'
    response = get_exception(index_link, msg)
    if response:
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


def get_exception(link_get, msg_get):
    """
    Fetches the content of the given URL and handles exceptions using the given error message.
    :param: link_get: str, the URL to fetch
    :param: msg_get: str, the error message to log in case of an exception
    :return: str or False, the response text if the request is successful, False if an exception occurs
    """
    response_get = False
    try:
        response_get = requests.get(link_get).text
    except requests.exceptions.RequestException as e:
        logging.error(f"{msg_get}: {e}")
    return response_get


def make_soup(link):
    """
    This function will provide the BeautifulSoup object for the scraping functions called on each recipe link.
    :param: str: link str
    :return: BeautifulSoup object
    """
    msg = 'Error making soup'
    response = get_exception(link, msg)
    if response:
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
    grid_elements = soup.find('div', class_='mntl-recipe-details__content')\
                        .find_all('div', class_='mntl-recipe-details__label')
    recipe_details = {}
    for element in grid_elements:
        label = element.text.strip()
        data = element.find_next_sibling(class_="mntl-recipe-details__value").text.strip()
        recipe_details[label] = data
    # convert the time to integer(minutes)
    for key, value in recipe_details.items():
        if 'Time' in key:
            recipe_details[key] = convert_to_minutes(value)
        elif key == 'Servings:' and value is not None:
            value = value.split()
            recipe_details[key] = int(value[0])
    return recipe_details


def convert_to_minutes(value_str):
    # Split the value string into parts
    parts = value_str.split()

    # Calculate the total time in minutes
    total_minutes = 0
    for i in range(0, len(parts), 2):
        value = int(parts[i])
        unit = parts[i+1]
        if unit == 'day' or unit == 'days':
            total_minutes += value * 24 * 60
        elif unit == 'mins' or unit == 'min':
            total_minutes += value
        elif unit == 'hours' or unit == 'hour' or unit == 'hrs':
            total_minutes += value * 60
        else:
            raise ValueError(f'Invalid time unit: {unit}')

    return total_minutes


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
            if key[-1] == 'g':
                key = key[:-1]
            nutrition_facts[value] = int(key)
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


def has_other_args(args):
    """
    Check if any other argument is provided alongside the 'all' flag.
    :param args: argparse.Namespace object containing the arguments
    :return: bool: True if any other argument is provided, False otherwise
    """
    return any([args.title, args.ingredients, args.details, args.reviews, args.rating, args.nutrition,
                args.published, args.category, args.link])


def setup_argparse():
    """
    Set up argparse arguments for the scraper.
    :return: parser: An argparse.ArgumentParser object with the configured arguments.
    """
    parser = argparse.ArgumentParser(description='Scrape data from allrecipes.com')
    parser.add_argument('--title', action='store_true', help='Scrape recipe title')
    parser.add_argument('--ingredients', action='store_true', help='Scrape recipe ingredients')
    parser.add_argument('--details', action='store_true', help='Scrape recipe details (prep time, cook time, etc.)')
    parser.add_argument('--reviews', action='store_true', help='Scrape number of reviews')
    parser.add_argument('--rating', action='store_true', help='Scrape recipe rating')
    parser.add_argument('--nutrition', action='store_true', help='Scrape nutrition facts')
    parser.add_argument('--published', action='store_true', help='Scrape publish date')
    parser.add_argument('--category', action='store_true', help='Scrape recipe category')
    parser.add_argument('--link', action='store_true', help='Get the link to the recipe')
    parser.add_argument('--all', action='store_true', help='Scrape all available data')

    return parser


def validate_args(parser):
    """
    Validate the arguments passed by the user.
    :param parser:  An argparse.ArgumentParser object with the configured arguments.
    :return: args_setter: A Namespace object containing the parsed arguments.
    """
    # Use parse_known_args() instead of parse_args() to flag unknown args
    args_setter, unknown_args = parser.parse_known_args()

    # Check if any arguments were passed
    if len(sys.argv) <= 1:
        message = 'No argument was passed'
        exit_gracefully(message, parser)

    # Check if too many arguments were passed
    elif len(sys.argv) > 10:
        message = 'Too many arguments'
        exit_gracefully(message, parser)

    # Check if unrecognized arguments were passed
    if unknown_args:
        message = f'Unrecognized arguments: {unknown_args}'
        exit_gracefully(message, parser)

    # Check if --all is provided with other arguments
    if args_setter.all and has_other_args(args_setter):
        message = '--all argument should not be used with other arguments'
        exit_gracefully(message, parser)

    # If user chooses to scrape all available data
    if args_setter.all:
        args_setter.title = args_setter.ingredients = args_setter.details = args_setter.reviews = args_setter.rating\
            = args_setter.nutrition = args_setter.published = args_setter.category = args_setter.link = True

    return args_setter


def exit_gracefully(msg, parser_exit):
    """
    Prints the argparse help message, logs an error message, and exits the program.
    :param msg: A string representing the error message to log.
    :param parser_exit: An ArgumentParser object used for printing the help message.
    """
    parser_exit.print_help()
    logging.error(msg)
    exit()


def argparse_setter():
    """
    Set up and validate the argparse arguments for the scraper.
    :return: args_setter: A Namespace object containing the parsed and validated arguments.
    """
    parser = setup_argparse()
    args_setter = validate_args(parser)
    return args_setter


def logging_setter():
    """
    Set up logging configuration
    :return: logging configuration
    """
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("logging_info.log"),
            logging.StreamHandler()
        ]
    )


def scraper(all_links_scraper, args_scraper):
    """
    Scrape recipe data from allrecipes.com based on the provided arguments.
    :param: all_links_scraper: A list of URLs to scrape for recipe data.
            args_scraper: A Namespace object containing the parsed and validated arguments from argparse.
    """
    count = 1
    with open('scraping.log', 'w+', encoding='utf-8') as output_file:
        for link in all_links_scraper:
            try:
                soup = make_soup(link)
                ingredients = get_ingredients(soup)

                # to avoid scraping web pages that aren't recipes
                if len(ingredients) == 0:
                    continue

                # call each scraping method based on the argparse arguments
                function_map = {
                    'title': get_title,
                    'ingredients': get_ingredients,
                    'details': get_recipe_details,
                    'reviews': get_num_reviews,
                    'rating': get_rating,
                    'nutrition': get_nutrition_facts,
                    'published': get_date_published,
                    'category': get_categories,
                    'link': lambda _: link
                }
                scraped_data = {key: func(soup) for key, func in function_map.items() if getattr(args_scraper, key)}

                # write scraped data to output file
                output_file.write(f'\nRecipe {count}:\n')
                for key, value in scraped_data.items():
                    output_file.write(f'{key.capitalize()}: {value}\n')
                output_file.write('\n')

                # logging info
                logging.info(f'Scraped recipe number: {count}\n')
                count += 1
            except Exception as e:
                logging.error(f'Error scraping recipe from link {link}: {e}')


def main():
    """
    Takes in the index link for allrecipes.com to begin scraping the site. Iterates over
    all recipe links and calls scraping functions on each of them. Iteration will skip over non-recipe web pages.
    :return: None: writes output to scraping.log file
    """

    logging_setter()
    index_links = get_index_links(SOURCE)
    all_links = get_all_links(index_links)
    args = argparse_setter()
    scraper(all_links, args)


if __name__ == '__main__':
    main()
