import logging
import openai
import json
import ast
import sql_connection as sq
import command_line as cl

with open('constants.json') as f:
    constants = json.load(f)


def api_query(ingredient):
    """
    Send a request to OpenAI's GPT-3 API to categorize a given ingredient into a two-key dictionary format.
    :param ingredient: str: A string of an ingredient and its amount in various units (unprocessed).
    :return: message_dict_str: 2 key dict:  string of categorized ingredient and its quantity in a 2 key dictionary.
    """
    openai.api_key = constants['API_KEY']

    prompt = f"Categorize this string:{ingredient} into a two-key dictionary format with the first " \
             f"key being 'quantity' and the second key being 'ingredient'. Convert the quantity in ounces " \
             f"or cups to grams, so that the value of the 'quantity' key is a float number, and simplify the " \
             f"ingredient names to their most basic forms. If a specific quantity or " \
             f"ingredient cannot be identified for a line, categorize the line with a quantity of 'None' " \
             f"and an ingredient of 'N/A'. Provide only one dictionary per string."
    try:
        response = openai.Completion.create(
            engine=constants['GPT_MODEL'],
            prompt=prompt,
            max_tokens=constants["MAX_TOKENS"],
            n=constants["N_GPT_COMPLETIONS"],
            stop=None,
            temperature=constants["GPT_TEMP"]
        )
    except Exception as e:
        raise Exception(f"An error occurred while querying the API: {e}")

    message = response.choices[constants["FIRST_RESPONSE"]].text
    message_dict_str = message[message.index("{"):message.rindex("}") + 1]
    print(message_dict_str)
    return message_dict_str


def process_ingredients_data(connection, cursor):
    """
    This function applies the processing of the api_query to each row of the unprocessed ingredients table.
    It marks each ingredient with a boolean, to avoid processing the same ingredient twice.
    :param connection: connects to sql
    :param cursor: executes sql queries
    :return: None
    """
    # Select unprocessed rows of 'ingredient' and 'recipe_id' columns from the specified table
    cursor.execute(f"SELECT ingredient, recipe_id, id FROM ingredients WHERE processed = 0")
    rows = cursor.fetchall()

    # Loop through each row and apply the 'api_query' function to the 'ingredient' column
    for row in rows:
        ingredient = row[0]
        recipe_id = row[1]
        id_for_processed_check = row[2]
        try:
            ingredients_quantity_dict = api_query(ingredient)
            insert_api_data(constants["CLEAN_DATA_TABLE_NAME"], ingredients_quantity_dict, recipe_id)
            # Update the 'processed' column to indicate that the row has been processed
            cursor.execute(f"UPDATE ingredients SET processed = 1 WHERE id = %s", (id_for_processed_check,))
            connection.commit()
        except Exception as ex:
            raise Exception(f"Error processing row with id {id_for_processed_check}: {ex}")
    connection.commit()
    connection.close()


def insert_api_data(table_name, ingredient, retrieved_recipe_id):
    """
    Inserts data into the table.
    :param table_name: The name of the table where data is to be inserted.
    :param ingredient: A two-key dictionary with keys 'quantity' and 'ingredient', or a tuple of such dictionaries.
    :param retrieved_recipe_id: The ID of the recipe in the 'recipes' table.
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()

    # split the modified ingredient string into a tuple of substrings
    if ingredient.count('{') > 1:
        ingredient = ingredient.replace('},', '} @')
        ingredient = tuple(ingredient.split('@'))

    # Convert the string representation of the ingredient dictionary or tuple to a Python object
    if isinstance(ingredient, str):
        ingredient = ast.literal_eval(ingredient)
        cursor.execute(f"INSERT INTO {table_name} (recipe_id, ingredient, quantity) VALUES (%s, %s, %s)",
                       (int(retrieved_recipe_id), ingredient['ingredient'], ingredient['quantity']))
        logging.info(f"Clean data inserted: ingredient: {ingredient['ingredient']}, quantity: {ingredient['quantity']}")

    # If the ingredient is a tuple of dictionaries, loop through the tuple and insert each dictionary as a separate row
    elif isinstance(ingredient, tuple):
        for ingredient_str in ingredient:
            ingredient_dict = ast.literal_eval(ingredient_str)
            cursor.execute(f"INSERT INTO {table_name} (recipe_id, ingredient, quantity) VALUES (%s, %s, %s)",
                           (int(retrieved_recipe_id), ingredient_dict['ingredient'], ingredient_dict['quantity']))
            logging.info(f"Clean data inserted: ingredient: ingredient: {ingredient_dict['ingredient']}, "
                         f"quantity: {ingredient_dict['quantity']}")
    connection.commit()
    connection.close()


def main():
    """
    Execute the functions above.
    :return: None
    """
    cl.logging_setter()
    connection = sq.sql_connector()
    cursor = connection.cursor()
    try:
        process_ingredients_data(connection, cursor)
    except Exception as exe:
        logging.error(exe)


if __name__ == "__main__":
    main()
