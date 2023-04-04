import requests
import logging
import json
from bs4 import BeautifulSoup


with open('constants.json') as f:
    constants = json.load(f)


def get_index_links(main_index_link):
    """
    Receives the source url and pulls the highest level urls from the index page.
    :param: str: url
    :return: list: urls
    """
    response = check_request_exception(main_index_link, get_index_links)
    if response:
        soup = BeautifulSoup(response, features="html.parser")
        a_tags = soup.find_all('a', class_=constants['INDEX_LINK_CLASS'])
        index_links = [a_tag['href'] for a_tag in a_tags]
        return index_links


def get_recipe_links(index_link):
    """
    Receives a link from the index_links and scrapes all the recipe urls from that page.
    :param: str: url
    :return: list: urls
    """
    response = check_request_exception(index_link, get_recipe_links)
    if response:
        soup = BeautifulSoup(response, features="html.parser")
        top_link_tags = soup.find_all('a', {
            'class': constants['TOP_LINK_CLASS']})
        top_links = [attr['href'] for attr in top_link_tags]
        bottom_link_tags = soup.find_all('a', class_=constants['BOTTOM_LINK_CLASS'])
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
    links = []
    for link in index_links:
        links.extend(get_recipe_links(link))
        logging.info(f'Links from: {link}  retrieved')
    all_links = list(set(links))
    return all_links


def check_request_exception(link, func_name):
    """
    Fetches the content of the given URL and handles exceptions using the given error message.
    :param: str: the URL to fetch
    :param: str: the error message to log in case of an exception
    :return: str or False, the response text if the request is successful, False if an exception occurs
    """
    response_get = False
    try:
        response_get = requests.get(link).text
    except requests.exceptions.RequestException as e:
        logging.error(f"Problem getting link {link} in {func_name.__name__}. Error: {e}")
    return response_get
