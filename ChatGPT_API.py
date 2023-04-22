import openai
import json
import sql_connection as sq

with open('constants.json') as f:
    constants = json.load(f)


def categorize_ingredients(table_name):
    """
    Retrieve all rows of 'ingredient' column from the specified table and apply the 'api_query' function to each row.
    :param table_name: The name of the table containing 'ingredient' column.
    :return: None
    """
    # Connect to the database
    connection = sq.sql_connector()
    cursor = connection.cursor()

    # Select all rows from the specified table
    cursor.execute(f"SELECT ingredient FROM {table_name}")
    rows = cursor.fetchall()

    # Loop through each row and apply the 'api_query' function to the 'ingredient' column
    for row in rows:
        ingredient = row[0]
        print(api_query(ingredient))

    # Close the database connection
    connection.close()


def api_query(ingredient):
    """
    Send a request to OpenAI's GPT-3 API to categorize a given ingredient into a two-key dictionary format.
    :param ingredient: A string of an ingredient.
    :return: A string of categorized ingredient in a two-key dictionary format.
    """
    # Load API key
    openai.api_key = constants['API_KEY']

    model_engine = constants['GPT_MODEL']

    prompt_in = f"Can you please categorize this string:{ingredient} into a two-key dictionary format with the first " \
                f"key being 'quantity' and the second key being 'ingredient'? Please convert the quantity in ounces " \
                f"or cups to grams, so that the value of the 'quantity' key is a float number and simplify the " \
                f"ingredient names to their most basic forms. If a specific quantity or " \
                f"ingredient cannot be identified for a line, please categorize the line with a quantity of 'None' " \
                f"and an ingredient of 'N/A'."

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_in,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )

    message = response.choices[0].text
    return message


def main():
    """
    Execute the functions above.
    :return: None
    """
    categorize_ingredients(constants['API_INGREDIENTS_TABLE'])


if __name__ == "__main__":
    main()
