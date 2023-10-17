# 🍲 AllRecipes Web Scraping Project

**Developers**: Dar Shabi & Maya Halevy

## 📌 Introduction
This project is focused on extracting recipe data from [Allrecipes.com](https://www.allrecipes.com), a renowned platform that offers a plethora of recipes spanning various cuisines and categories. Our objective is to curate this data into a structured format, making it accessible for further analysis and utilization.

## 🛠 Tools & Libraries
- **Web Scraping Libraries**: Beautiful Soup, Requests, and Regex (Refer to `requirements.txt` for specific versions).
- **Data Processing**: ChatGPT's API was crucial in standardizing the ingredients table. Raw data often contained a mixture of food items, descriptive terms, units of measurement, and instructions. Our post-processing ensured the data only retained the ingredient name and its corresponding quantity in grams.

## 🌐 Target Website & Data Collection
- **Website Index**: [AllRecipes A-Z Index](https://www.allrecipes.com/recipes-a-z-6735880)
    - This is the primary link referenced in our script. It's hard-coded as a constant for easy access.

- **Attributes Extracted**:
    - Recipe Title
    - Ingredients
    - Recipe Details (e.g., Prep Time, Cook Time)
    - Review Count & Recipe Rating
    - Nutrition Facts
    - Publication Date
    - Recipe Category (e.g., Main Dish, Breakfast)

- **Outputs**:
    - The script generates two files in the working directory:
        1. Logging Statements
        2. Scraped Data 

> **Note**: While extracting, we noticed some non-recipe URLs classified under the same HTML class as valid recipes. We refined our extraction criteria to focus solely on pages featuring an ingredients section.

## ⚙ CLI Arguments
Our scraper offers a suite of CLI arguments to customize the data extraction process. Below are the available arguments:

- `--title`: Extract the recipe title.
- `--ingredients`: Extract the ingredients list.
- `--details`: Fetch recipe details such as prep time.
- `--reviews`: Retrieve the number of reviews.
- `--rating`: Determine the recipe rating.
- `--nutrition`: Get nutrition-related data.
- `--published`: Fetch the publication date.
- `--category`: Pinpoint the recipe category.
- `--link`: Secure the direct link to the recipe.
- `--instructions`: Extract the recipe's preparation steps.
- `--all`: Extract all available attributes.

> **Note**: By default, the scraper won't fetch any data. It's essential to specify desired attributes using the arguments.

## 🗄 Database Integration
- **Platform**: MySQL 
- **Database Model**: The ERD can be viewed [here](https://github.com/DarShabi/Web-Scraping-allrecipes/blob/main/ERD%20Milestone%203.jpg).

### Setting up the Database
1. Before utilizing our web scraper, ensure the database is correctly set up. Use the `database_creation.py` script to instantiate the requisite database schema.
2. Ensure you have the MySQL connector for Python installed.
3. Modify the connection parameters in `sql_connector()` (located in `sql_connection.py`) to mirror your MySQL configuration.
4. Execute `database_creation.py` for initial database configuration.

## 🚀 How to Run the Code

- Ensure `sql_connection.py` (which provides the `sql_connector()` function for database connectivity) resides in the same directory as `database_creation.py`.
- Before invoking the main scraper, locally run `database_creation.py` for proper database initialization.
- Remember: The ChatGPT API isn't free. The provided API KEY in the constants file might not be universally functional. Users need to procure their own unique key.

---

Good Luck with your culinary data adventures! 🥘
