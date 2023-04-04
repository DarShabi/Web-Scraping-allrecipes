
# AllRecipes Web Scraping Project
### Dar Shabi, Maya Halevy


The target website for this project is Allrecipes.com, which is a popular recipe website that contains a wide range of recipes from different cuisines and categories. The project aims to scrape recipe data from this website and store it in a database for further analysis and use.

We used python's Beautiful Soup, Requests, and Regex libraries to scrape the allrecipes website (see requirements.txt for versions). We did not need to establish a hidden user nor did we face any site-related obstacles while scraping.

**AllRecipes Index Link**: https://www.allrecipes.com/recipes-a-z-6735880

This is the only link needed to run the script, it is included in the python code as a constant. 

#### Parameters collected: 
- Recipe Title
- Ingredients
- recipe details (e.g. Prep Time, Cook Time, etc.)
- Number of Reviews, Recipe Rating
- Nutrition Facts
- Date published
- Recipe Category (e.g. Main Dish, Breakfast)

The code creates two logfiles as output. One contains logging info statements, and the other contains the scraped data. These files are written to the current working directory. 

**Note**: This code has been modified for testing purposes. To scrape the entire allrecipes website, remove the slice on the return statement of the get_index_links function. 


We opted to use ‘html parser’ instead of ‘lxml’ as it might not work on all computers, but they can be used interchangeably.

There were some non-recipe urls listed with the same html tags as the recipe urls. We addressed this problem by only scraping websites with an ingredients list. This effectively filtered out the non-recipe websites. 

#### CLI Arguments

The scraper provides several CLI arguments that allow you to scrape specific data from allrecipes.com. The following arguments are available:

* --title: scrape the recipe title.
* --ingredients: scrape the recipe ingredients.
* --details: scrape recipe details (prep time, cook time, etc.).
* --reviews: scrape the number of reviews.
* --rating: scrape the recipe rating.
* --nutrition: scrape the nutrition facts.
* --published: scrape the publish date.
* --category: scrape the recipe category.
* --link: get the link to the recipe.
* --instructions: get the instructions of the recipe.
* --all: scrape all available data.
By default, none of the arguments are enabled. You need to specify which data you want to scrape by providing the corresponding argument

#### Database Documentation
This scraper stores data in a MySQL database. The ERD for the database:

![ERD](https://user-images.githubusercontent.com/127299167/229867995-72a70735-bb5b-4893-8a0b-0f193306bf1e.png)


#### Setting up the Database
To use this web scraper, you need to first set up the database. We have provided a script `database_creation.py` that creates the necessary database schema. Before running the script, make sure that you have the required MySQL connector for Python installed. You also need to update the connection details in the `sql_connector()` function inside `sql_connection.py` to match your local MySQL database setup.

Once you have updated the connection details, you can run the database_creation.py script to create the Recipes database and the necessary tables for the scraper.

Note that `sql_connection.py` is a necessary file that provides the `sql_connector()` function that connects to the MySQL database. Make sure that you have it in the same directory as `database_creation.py`.
