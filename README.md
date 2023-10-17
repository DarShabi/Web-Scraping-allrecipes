# 🍲 AllRecipes Web Scraping Project

**Developers**: Dar Shabi & Maya Halevy

## 📌 Introduction
This project is focused on extracting recipe data from [Allrecipes.com](https://www.allrecipes.com), a popular platform that offers a variety of recipes posted by its users. Our objective is to collect and process this data into a structured format, making it accessible for further analysis and api enrichment.

## 🛠 Tools & Libraries
- **Web Scraping Libraries**: Beautiful Soup, Requests, and Regex (Refer to `requirements.txt` for specific versions).
- **Data Processing**: ChatGPT's API was crucial in standardizing the ingredients table. The raw data often contained a mixture of food items, descriptive terms, units of measurement, and instructions. Our post-processing ensured the data only retained the ingredient name and its corresponding quantity in grams.

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

> **Note**: We noticed that non-recipe URLs were classified under the same HTML class as valid recipes. We refined our extraction criteria to focus solely on pages featuring an ingredients section.

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

> **Note**: By default, the scraper does not fetch any data. You need to specify which data you want to scrape by providing the corresponding argument.

## 🗄 Database Integration
- **Platform**: MySQL 
- **Database Model**: The ERD can be viewed [here](https://github.com/DarShabi/Web-Scraping-allrecipes/blob/main/ERD%20Milestone%203.jpg).

## How to Run the Code
- Before running the main scraper, locally run `database_creation.py` to initialize the database.
- Ensure you have the MySQL connector for Python installed.
- Modify the connection parameters in `sql_connector()` (located in `sql_connection.py`) to mirror your MySQL configuration.
- Check that `sql_connection.py` (which provides the `sql_connector()` function for database connectivity) resides in the same directory as `database_creation.py`.
- Remember: The ChatGPT API is a paid service. The provided API KEY in the constants file is not be universally functional. 

---

