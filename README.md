
# AllRecipes Web Scraping Project
### Dar Shabi, Maya Halevy
\
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
This scraper stores data in a MySQL database. The EDR for the database:

![ERD](https://user-images.githubusercontent.com/127299167/229867995-72a70735-bb5b-4893-8a0b-0f193306bf1e.png)


#### Schema Installation
*  Modify the `sql_connector()` function in `sql_connection.py` with your own database credentials before running the program.
*  Run the program with the command `python database_creation.py`.
