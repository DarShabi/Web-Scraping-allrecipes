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
import constants as c
import scrape_links as s
import command_line as ar


def make_soup(link):
    """
    This function will provide the BeautifulSoup object for the scraping functions called on each recipe link.
    :param: str: link str
    :return: BeautifulSoup object
    """
    response = s.check_request_exception(link, make_soup)
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
    p_tags = soup.find_all("ul", class_=c.INGREDIENTS_CLASS)
    for p in p_tags:
        ingredients.append(p.text.strip())
    if not len(ingredients):
        return ingredients
    ingredients = ''.join(ingredients).replace('\n\n\n', ' ?').split('?')
    return ingredients


def get_recipe_details(soup):
    """
    Scrapes the recipe details (e.g., "Prep Time", "Cook Time", etc.) and returns then as a dictionary.
    :param: BeautifulSoup object
    :return: dict: recipe_details
    """
    grid_elements = soup.find('div', class_=c.DETAILS_CONTENT) \
        .find_all('div', class_=c.DETAILS_LABEL)
    recipe_details = {}
    for element in grid_elements:
        label = element.text.strip()
        data = element.find_next_sibling(class_=c.DETAILS_VALUE).text.strip()
        recipe_details[label] = data
    for key, value in recipe_details.items():  # convert the time and number of servings to int
        if c.TIME in key:
            recipe_details[key] = convert_to_minutes(value)
        elif key == c.SERVINGS and value.isdigit():
            recipe_details[key] = int(value)
    return recipe_details


def convert_to_minutes(value_str):
    values_list = value_str.split()
    total_minutes = 0
    for i in range(0, len(values_list), c.NEXT_PAIR):
        value = int(values_list[i])
        unit = values_list[i + c.NEXT_INDEX]
        if unit == 'day' or unit == 'days':
            total_minutes += value * c.HOURS * c.MINS
        elif unit == 'mins' or unit == 'min':
            total_minutes += value
        elif unit == 'hours' or unit == 'hour' or unit == 'hrs':
            total_minutes += value * c.MINS
        else:
            raise ValueError(f'Invalid time unit: {unit}')
    return total_minutes


def get_num_reviews(soup):
    """
    Returns the number of reviews on each recipe as an integer.
    :param: BeautifulSoup object
    :return: str: number of reviews
    """
    num_reviews_elem = soup.find('div', {'id': c.REVIEWS_CLASS}).text
    if any(char.isdigit() for char in num_reviews_elem):
        num_reviews = "".join([i for i in num_reviews_elem if i.isnumeric()])
    else:
        num_reviews = c.NO_REVIEWS
    return num_reviews


def get_rating(soup):
    """
    Returns the rating of the recipe as a float. If there are no reviews on the recipe, will
    return the rating as NoneType object.
    :param: BeautifulSoup object
    :return: float: recipe rating or None
    """
    rating_elem = soup.find('div', {'id': c.RATING_CLASS})
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
    nutrition_table = soup.find('table', class_=c.NUTRITION_CLASS)
    nutrition_facts = {}
    for row in nutrition_table.find_all('tr'):
        cells = row.find_all('td')
        amount = cells[c.AMOUNT_INDEX].text.strip().lower()
        label = cells[c.LABEL_INDEX].text.strip()
        if c.GRAMS in amount:
            amount = amount[:c.GRAMS_INDEX]
        nutrition_facts[label] = int(amount)
    return nutrition_facts


def get_date_published(soup):
    """
    Extracts the date that the recipe was published on allrecipes.com
    :param: BeautifulSoup object
    :return: datetime object: date_published
    """
    date_elem = soup.find('div', class_=c.DATE_CLASS).text.strip().split()
    date_published_str = " ".join(date_elem[c.PUBLISHED_ON:])
    date_published = datetime.datetime.strptime(date_published_str, '%B %d, %Y')
    return date_published


def get_categories(soup):
    """
    Gets the categories of the recipe (e.g. breakfast, main dish, vegan) and returns them as a list of strings.
    :param: BeautifulSoup object
    :return: list: categories
    """
    breadcrumb = soup.find('ul', class_=c.CATEGORY_CLASS)
    categories = [elem.text.strip() for elem in breadcrumb.find_all('li')]
    return categories


def scraper(all_links_scraper, args_scraper):
    """
    Scrape recipe data from allrecipes.com based on the provided arguments.
    :param: all_links_scraper: A list of URLs to scrape for recipe data.
            args_scraper: A Namespace object containing the parsed and validated arguments from argparse.
    """
    recipes_scraped = 1
    with open('scraping.log', 'w+', encoding='utf-8') as output_file:
        for link in all_links_scraper:
            try:
                soup = make_soup(link)
                ingredients = get_ingredients(soup)
                if not len(ingredients):
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
                output_file.write(f'\nRecipe {recipes_scraped}:\n')
                for key, value in scraped_data.items():
                    output_file.write(f'{key.capitalize()}: {value}\n')
                output_file.write('\n')

                # logging info
                logging.info(f'Scraped recipe number: {recipes_scraped}\n')
                recipes_scraped += 1
            except Exception as e:
                logging.error(f'Error scraping recipe details from link {link}: {e}')


def main():
    """
    Takes in the index link for allrecipes.com to begin scraping the site. Iterates over
    all recipe links and calls scraping functions on each of them. Iteration will skip over non-recipe web pages.
    :return: None: writes output to scraping.log file
    """

    ar.logging_setter()
    index_links = s.get_index_links(c.SOURCE)
    all_links = s.get_all_links(index_links)
    args = ar.argparse_setter()
    scraper(all_links, args)


if __name__ == '__main__':
    main()
