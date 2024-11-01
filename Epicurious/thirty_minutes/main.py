"""
Scrapes recipes from https://www.epicurious.com/recipes-menus/30-minute-meals-gallery to a csv file.

Script theoretically works, BUT every time it crashes at different site. Crashing seems pretty random and i don't know why.
I would say the site could be scaped fine in smaller batches. Scraping in one take for me always ended up in some exception. 
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

def main():
    options = Options()
    # Don't show UI
    options.add_argument("--headless")
    # Open browser
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.epicurious.com/recipes-menus/30-minute-meals-gallery")
    # Bypass cookies popup
    cookies_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
    cookies_btn.click()

    _ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='BaseButton']")))
    buttons = driver.find_elements(By.CSS_SELECTOR, "[class*='BaseButton']")
    # Keep just buttons for recipes
    recipes_buttons = [btn for btn in buttons if btn.text == "GET THIS RECIPE"]
    # Extract links for the recipes
    links = [btn.get_attribute("href") for btn in recipes_buttons]
    
    all_names = []
    all_ingredients = []
    all_preparations = []
    all_ratings = []
    all_tags = []

    # If exception occurs terminate the driver
    try:
        for link in links:
            driver.get(link)

            name = driver.find_element(By.CSS_SELECTOR, "[data-testid='ContentHeaderHed']").text
            all_names.append(name)

            print(name)

            ingredients_div = driver.find_element(By.CSS_SELECTOR, "[data-testid='IngredientList']")
            ingredients = ingredients_div.find_elements(By.CSS_SELECTOR, "[class*='Description']")
            all_ingredients.append([ing.text for ing in ingredients])

            preparation_div = driver.find_element(By.CSS_SELECTOR, "li[class*='InstructionListWrapper']")
            preparation = preparation_div.find_elements(By.TAG_NAME, "p")
            all_preparations.append([prep.text for prep in preparation])

            rating_div = driver.find_element(By.CSS_SELECTOR, "[class*='RatingFormWrapper']")
            rating = rating_div.find_element(By.TAG_NAME, "p").text
            all_ratings.append(rating)

            tags = driver.find_elements(By.CSS_SELECTOR, "[class*='TagCloudName']")
            all_tags.append([tag.text for tag in tags])
    finally:
        driver.quit()

    # Save the data
    df = pd.DataFrame({
        "Name": all_names,
        "Ingredients": all_ingredients,
        "Preparation": all_preparations,
        "Rating": all_ratings,
        "Tags": all_tags
    })

    df.to_csv("30_minutes_recipes.csv", index=False)


if __name__ == "__main__":
    main()