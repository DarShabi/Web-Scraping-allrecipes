
# AllRecipes Web Scraping Project
### Dar Shabi, Maya Halevy
\
We used python's Beautiful Soup, Requests, and Regex libraries to scrape the allrecipes website (see requirements.txt for versions). We did not need to establish a hidden user nor did we face any site-related obstacles while scraping.

##### AllRecipes Index link: https://www.allrecipes.com/recipes-a-z-6735880
This is the only link needed to run the script, it is included in the python code as a constant. 

#### Parameters collected: 
- Recipe Title
- Ingredients
- recipe details (e.g. Prep Time, Cook Time, etc.)
- Number of Reviews, Recipe Rating
- Nutrition Facts
- Date published
- Recipe Category (e.g. Main Dish, Breakfast)

We opted to use ‘html parser’ instead of ‘lxml’ as it might not work on all computers, but they can be used interchangeably.

There were some non-recipe urls listed with the same html tags as the recipe urls. We addressed this problem by only scraping websites with an ingredients list. This effectively filtered out the non-recipe websites. 

