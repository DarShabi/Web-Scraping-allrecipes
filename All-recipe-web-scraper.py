"""
This .py file scrapes the allrecipes website using python's beautiful soup, requests, and regex libraries for
various data points. The parameters we are collecting are Recipe Title, Ingredients, recipe details (Prep Time,
Cook Time, etc.), Number of Reviews, Recipe Rating, Nutrition Facts, Date published, and
Recipe Category (e.g. Main Dish, Breakfast).
"""
from bs4 import BeautifulSoup
import re
import logging
import datetime
import json
import scrape_links as s
import command_line as ar
import dump_data as dd

with open('constants.json') as f:
    constants = json.load(f)


def make_soup(link):
    """
    This function will provide the BeautifulSoup object for the scraping functions called on each recipe link.
    :param: str: link str
    :return: BeautifulSoup object
    """
    try:
        response = s.check_request_exception(link, make_soup)
        soup = BeautifulSoup(response, features="html.parser")
        return soup
    except Exception as e:
        logging.error(f'Error getting response from link {link}: {e}')
        return None


def get_title(soup):
    """
    Scrapes the title from each recipe page.
    :param: BeautifulSoup object
    :return: str: recipe title
    """
    try:
        title = soup.title.string
    except Exception as e:
        logging.error(f'Error getting title: {e}')
        return None
    return title


def get_ingredients(soup):
    """
    Scrapes the ingredients, returns a list of strings with each ingredient and its quantity. To filter out
    non-recipe web pages, if there are no ingredients listed, will just return an empty list.
    :param: BeautifulSoup object
    :return: list: ingredients
    """
    ingredients = []
    try:
        p_tags = soup.find_all("ul", class_=constants['INGREDIENTS_CLASS'])
    except Exception as e:
        logging.error(f'Error getting ingredients: {e}')
        return None
    for p in p_tags:
        ingredients.append(p.text.strip())
    if not len(ingredients):
        return ingredients
    ingredients = ''.join(ingredients).replace('\n\n\n', ' ?').split('?')
    return ingredients


def fetch_grid_elements_for_recipe_details(soup):
    """
    This function gets the grid elements in the recipe details section from the web page
    :param soup: BeautifulSoup object
    :return: html grid elements
    """
    try:
        grid_elements = soup.find('div', class_=constants['DETAILS_CONTENT']) \
            .find_all('div', class_=constants['DETAILS_LABEL'])
        return grid_elements
    except Exception as e:
        logging.error(f'Error getting recipe details label: {e}')
        return None


def extract_label_recipe_details(element):
    """
    This function takes in the grid element and scrapes the details value from the web page
    :param element html
    :return: tuple of the label its data
    """
    label = element.text.strip()
    try:
        value = element.find_next_sibling(class_=constants['DETAILS_VALUE']).text.strip()
        return label, value
    except Exception as e:
        logging.error(f'Error recipe details value: {e}')
        return None, None


def process_recipe_details(intermediate_details):
    """
    This function takes in the recipe details and makes the times and servings into consistent values
    :param intermediate_details:
    :return: dict: intermediate_details
    """
    for key, value in intermediate_details.items():
        try:
            if constants['TIME'] in key:
                intermediate_details[key] = convert_to_minutes(value)
            elif key == constants['SERVINGS'] and value.isdigit():
                intermediate_details[key] = int(value)
        except Exception as e:
            logging.error(f'Error processing recipe details: {e}')
            return None
    return intermediate_details


def get_recipe_details(soup):
    """
    Scrapes the recipe details (e.g., "Prep Time", "Cook Time", etc.) by calling fetch_grid_elements and extract_label helper functiions
    Also calls a processing function so that dictionary has the correct and standardized recipe details
    :param: BeautifulSoup object
    :return: dict: recipe_details
    """
    grid_elements = fetch_grid_elements_for_recipe_details(soup)
    if grid_elements is None:
        return None

    intermediate_details = {}
    for element in grid_elements:
        label, data = extract_label_recipe_details(element)
        if label is not None and data is not None:
            intermediate_details[label] = data

    recipe_details = process_recipe_details(intermediate_details)
    return recipe_details


def convert_to_minutes(value_str):
    """
    Converts a time value string to the equivalent time in minutes.
    :param value_str: The time value string to be converted.
    :return: The total time in minutes (int).
    :raise: ValueError: If the time unit is invalid.
    """
    values_list = value_str.split()
    total_minutes = 0

    try:
        for i in range(0, len(values_list), constants['NEXT_PAIR']):
            value = int(values_list[i])
            unit = values_list[i + constants['NEXT_INDEX']]
            if unit == 'day' or unit == 'days':
                total_minutes += value * constants['HOURS'] * constants['MINS']
            elif unit == 'mins' or unit == 'min':
                total_minutes += value
            elif unit == 'hours' or unit == 'hour' or unit == 'hrs':
                total_minutes += value * constants['MINS']
            else:
                raise ValueError(f'Invalid time unit: {unit}')
    except Exception as e:
        logging.error(f'Error converting recipe details to minutes: {e}')
        return None
    return total_minutes


def get_num_reviews(soup):
    """
    Returns the number of reviews on each recipe as an integer.
    :param: BeautifulSoup object
    :return: str: number of reviews
    """
    try:
        num_reviews_elem = soup.find('div', {'id': constants['REVIEWS_CLASS']}).text
        if any(char.isdigit() for char in num_reviews_elem):
            num_reviews = "".join([i for i in num_reviews_elem if i.isnumeric()])
        else:
            num_reviews = constants['NO_REVIEWS']
    except Exception as e:
        logging.error(f'Error scraping number of reviews: {e}')
        return None
    return num_reviews


def get_rating(soup):
    """
    Returns the rating of the recipe as a float. If there are no reviews on the recipe, will
    return the rating as NoneType object.
    :param: BeautifulSoup object
    :return: float: recipe rating or None
    """
    rating_elem = soup.find('div', {'id': constants['RATING_CLASS']})
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
    nutrition_table = soup.find('table', class_=constants['NUTRITION_CLASS'])
    nutrition_facts = {}

    if nutrition_table is not None:
        try:
            for row in nutrition_table.find_all('tr'):
                cells = row.find_all('td')
                amount = cells[constants['AMOUNT_INDEX']].text.strip().lower()
                label = cells[constants['LABEL_INDEX']].text.strip()
                if constants['GRAMS'] in amount:
                    amount = amount[:constants['GRAMS_INDEX']]
                nutrition_facts[label] = int(amount)
        except Exception as e:
            logging.error(f'Error scraping nutrition facts: {e}')
            return None
    return nutrition_facts

def get_date_published(soup):
    """
    Extracts the date that the recipe was published on allrecipes.com
    :param: BeautifulSoup object
    :return: datetime object: date_published
    """
    try:
        date_elem = soup.find('div', class_=constants['DATE_CLASS']).text.strip().split()
        date_published_str = " ".join(date_elem[constants['PUBLISHED_ON']:])
        date_published = datetime.datetime.strptime(date_published_str, '%B %d, %Y')
    except Exception as e:
        logging.error(f'Error scraping date published: {e}')
        return None
    return date_published


def get_categories(soup):
    """
    Gets the categories of the recipe (e.g. breakfast, main dish, vegan) and returns them as a list of strings.
    :param: BeautifulSoup object
    :return: list: categories
    """
    try:
        breadcrumb = soup.find('ul', class_=constants['CATEGORY_CLASS'])
        categories = [elem.text.strip() for elem in breadcrumb.find_all('li')]
    except Exception as e:
        logging.error(f'Error scraping recipe categories: {e}')
        return None
    return categories


def get_recipe_instructions(soup):
    """
    Extracts the recipe instructions from a BeautifulSoup object.
    :param: soup: BeautifulSoup object
    :return: dict: recipe instructions with numbered keys
    """
    instructions = {}
    instructions_elem = soup.find('ol', class_=constants['INSTRUCTIONS_CLASS'])
    try:
        for idx, tag in enumerate(instructions_elem.find_all('li')):
            # Remove the undesired text
            nested_elem = tag.find(class_='PHOTO_CAPTION_CLASS')
            if nested_elem:
                nested_elem.extract()
            instructions[idx+1] = tag.text.strip()
    except Exception as e:
        print(f"error getting instructions {e}")

    return instructions


def scraper(all_links, args):
    for link in all_links:
        try:
            soup = make_soup(link)
            scraped_data = scrape_data_from_soup(soup, args, link)
            write_data_to_database(scraped_data)
        except Exception as e:
            logging.error(f'Error scraping recipe details from link {link}: {e}')


def scrape_data_from_soup(soup, args, link):
    ingredients = get_ingredients(soup)
    if not len(ingredients):
        return {}

    function_map = {
        'title': get_title,
        'ingredients': get_ingredients,
        'details': get_recipe_details,
        'reviews': get_num_reviews,
        'rating': get_rating,
        'nutrition': get_nutrition_facts,
        'published': get_date_published,
        'category': get_categories,
        'link': lambda _: str(link),
        'instructions': get_recipe_instructions
    }
    scraped_data_with_nulls = {key: func(soup) for key, func in function_map.items() if getattr(args, key)}

    # Filter out None values
    scraped_data = {k: v for k, v in scraped_data_with_nulls.items() if v is not None}

    return scraped_data


def write_data_to_database(scraped_data):
    if not scraped_data:
        return
    try:
        dd.write_to_database(scraped_data)
        logging.info(f'Recipe: {scraped_data["title"]} was Inserted to the Recipes database.')
    except Exception as exc:
        logging.error(f'Error executing SQL: {exc}')


def main():
    """
    Takes in the index link for allrecipes.com to begin scraping the site. Iterates over
    all recipe links and calls scraping functions on each of them. Iteration will skip over non-recipe web pages.
    :return: None: writes output to scraping.log file
    """
    ar.logging_setter()
    index_links = s.get_index_links(constants['SOURCE'])
    all_links = s.get_all_links(index_links)
    args = ar.argparse_setter()
    scraper(all_links, args)


if __name__ == '__main__':
    main()
