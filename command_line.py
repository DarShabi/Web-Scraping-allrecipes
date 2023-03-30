import logging
import argparse
import sys
import constants as c


def has_other_args(args):
    """
    Check if any other argument is provided alongside the 'all' flag.
    :param args: argparse.Namespace object containing the arguments
    :return: bool: True if any other argument is provided, False otherwise
    """
    return any([args.title, args.ingredients, args.details, args.reviews, args.rating, args.nutrition,
                args.published, args.category, args.link, args.instructions])


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
    parser.add_argument('--instructions', action='store_true', help='Get the instructions of the recipe')
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
    if len(sys.argv) <= c.MIN_ARGS:
        message = 'No argument was passed'
        exit_gracefully(message, parser)

    # Check if too many arguments were passed
    elif len(sys.argv) > c.MAX_ARGS:
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
        args_setter.title = args_setter.ingredients = args_setter.details = args_setter.reviews = args_setter.rating \
            = args_setter.nutrition = args_setter.published = args_setter.category = args_setter.link\
            = args_setter.instructions = True

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
        handlers=[logging.FileHandler("logging_info.log", mode='w+'), logging.StreamHandler()]
    )
