"""
Scrapes information about turtles from https://www.scrapethissite.com/pages/frames/ to a csv file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

import csv
import re

def main():
    # Open browser
    driver = webdriver.Firefox()
    driver.get("https://www.scrapethissite.com/pages/frames/")
    # Focus the frame html code
    driver.switch_to.frame("iframe")
    # Find number of turtles
    TURTLES = len(driver.find_elements(By.CLASS_NAME, "btn"))

    # Variables for scraped data
    names = []
    alter_names = []
    years = []
    discoverers = []

    for i in range(TURTLES):
        # Load buttons
        buttons = driver.find_elements(By.CLASS_NAME, "btn")
        # Open turtle info
        buttons[i].click()

        names.append(driver.find_element(By.CLASS_NAME, "family-name").text)
        alter_names.append(driver.find_element(By.CLASS_NAME, "common-name").text)
        # Get all of the info text (bcs year of discovery and discoverer aren't in tags)
        text = driver.find_element(By.CLASS_NAME, "lead").text
        # Find year in the text
        years.append(re.search(r"\d+", text).group())
        # Find discoverer name in the text
        discoverers.append(re.search(r"by\s+([A-Za-z]+)\.", text).group(1))
        
        # Load back the main page
        driver.get("https://www.scrapethissite.com/pages/frames/")
        driver.switch_to.frame("iframe")

    driver.quit()

    # Open csv file to save extracted data
    with open("turtles.csv", "w", encoding="utf-8") as file:

        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        # First row (titles)
        writer.writerow(["Name", "Alter names", "Year", "Discoverer"])

        for name, alter, year, discoverer in zip(names, alter_names, years, discoverers):
            writer.writerow([name, alter, year, discoverer])






if __name__ == "__main__":
    main()