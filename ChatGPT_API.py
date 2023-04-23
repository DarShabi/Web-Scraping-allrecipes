import logging
import openai
import json
import ast
import sql_connection as sq
import command_line as cl

with open('constants.json') as f:
    constants = json.load(f)


def create_table(table_name):
    """
    Creates a table with the given name in the Recipe database.
    :param table_name: Name of the table to be created.
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, recipe_id INT, "
                   f"ingredient VARCHAR(255), quantity FLOAT)")
    connection.commit()
    connection.close()


def api_query(ingredient):
    """
    Send a request to OpenAI's GPT-3 API to categorize a given ingredient into a two-key dictionary format.
    :param ingredient: A string of an ingredient.
    :return: A string of categorized ingredient in a two-key dictionary format.
    """
    # Load API key
    openai.api_key = constants['API_KEY']

    prompt_in = f"Can you please categorize this string:{ingredient} into a two-key dictionary format with the first " \
                f"key being 'quantity' and the second key being 'ingredient'? Please convert the quantity in ounces " \
                f"or cups to grams, so that the value of the 'quantity' key is a float number and simplify the " \
                f"ingredient names to their most basic forms. If a specific quantity or " \
                f"ingredient cannot be identified for a line, please categorize the line with a quantity of 'None' " \
                f"and an ingredient of 'N/A'. Please provide only one dictionary per string."
    try:
        response = openai.Completion.create(
            engine=constants['GPT_MODEL'],
            prompt=prompt_in,
            max_tokens=constants["MAX_TOKENS"],
            n=constants["N_GPT_COMPLETIONS"],
            stop=None,
            temperature=constants["GPT_TEMP"]
        )
    except Exception as e:
        raise Exception(f"An error occurred while querying the API: {e}")

    message = response.choices[constants["GPT_CHOICE"]].text
    message_dict_str = message[message.index("{"):message.rindex("}") + 1]
    return message_dict_str


def process_ingredients_data(table_name):
    """
    Retrieve all rows of 'ingredient' column from the specified table and apply the 'api_query' function to each row.
    :param table_name: The name of the table containing 'ingredient' column.
    :return: None
    """
    # Connect to the database
    connection = sq.sql_connector()
    cursor = connection.cursor()
    # Check if 'processed' column exist
    cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'processed'")
    result = cursor.fetchone()

    # create 'processed' column if not exist
    if result is None:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN processed BOOLEAN DEFAULT 0")

    # Select unprocessed rows of 'ingredient' and 'recipe_id' columns from the specified table
    cursor.execute(f"SELECT ingredient, recipe_id, id FROM {table_name} WHERE processed = 0")
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
            cursor.execute(f"UPDATE {table_name} SET processed = 1 WHERE id = %s", (id_for_processed_check,))
            connection.commit()  # Add a commit after updating the 'processed' column
        except Exception as ex:
            raise Exception(f"Error processing row with id {id_for_processed_check}: {ex}")
    # Close the database connection
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
    if ingredient.count('{') > 1:
        ingredient = ingredient.replace('},', '} @')
        ingredient = tuple(ingredient.split('@'))

    # Convert the string representation of the ingredient dictionary or tuple to a Python object
    if isinstance(ingredient, str):
        ingredient = ast.literal_eval(ingredient)
        cursor.execute(f"INSERT INTO {table_name} (recipe_id, ingredient, quantity) VALUES (%s, %s, %s)",
                       (int(retrieved_recipe_id), ingredient['ingredient'], ingredient['quantity']))
        logging.info(f"Clean data inserted to: "
                     f"{ constants['CLEAN_DATA_TABLE_NAME'] }, "
                     f"ingredient: {ingredient['ingredient']}, "
                     f"quantity: {ingredient['quantity']}")

    # If the ingredient is a tuple of dictionaries, loop through the tuple and insert each dictionary as a separate row
    elif isinstance(ingredient, tuple):
        for ingredient_str in ingredient:
            ingredient_dict = ast.literal_eval(ingredient_str)
            cursor.execute(f"INSERT INTO {table_name} (recipe_id, ingredient, quantity) VALUES (%s, %s, %s)",
                           (int(retrieved_recipe_id), ingredient_dict['ingredient'], ingredient_dict['quantity']))
            logging.info(f"Clean data inserted to: "
                         f"{constants['CLEAN_DATA_TABLE_NAME']}, "
                         f"ingredient: {ingredient_dict['ingredient']}, "
                         f"quantity: {ingredient_dict['quantity']}")
    connection.commit()
    connection.close()


def main():
    """
    Execute the functions above.
    :return: None
    """
    cl.logging_setter()
    create_table(constants["CLEAN_DATA_TABLE_NAME"])
    try:
        process_ingredients_data(constants['UNPROCESSED_INGREDIENTS_TABLE'])
    except Exception as exe:
        logging.error(exe)


if __name__ == "__main__":
    main()
