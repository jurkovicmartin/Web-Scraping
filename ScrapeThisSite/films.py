"""
Scrapes oscar winning films from https://www.scrapethissite.com/pages/ajax-javascript/ to a csv file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv


def main():

    # Open csv file to save extracted data
    with open("films.csv", "w", encoding="utf-8") as file:

        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        # First row (titles)
        writer.writerow(["Year", "Title", "Nominations", "Awards", "Best picture"])

        driver = webdriver.Firefox()
        # Load tha page
        driver.get("https://www.scrapethissite.com/pages/ajax-javascript/")

        for year in range(2010, 2016):
            # Find link to load the content to scrap
            link = driver.find_element(By.LINK_TEXT, str(year))
            link.click()
            
            # Other than first pass
            if year != 2010:
                # Wait for the "film-title" class to be stable
                WebDriverWait(driver, 10).until(EC.staleness_of(driver.find_element(By.CLASS_NAME, "film-title")))

            # Wait for dynamically loaded content (detect loading of "film-title" class)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "film-title")))

            html = driver.page_source

            soup = BeautifulSoup(html, "html.parser")
            # Extract data
            titles = soup.find_all("td", attrs={"class":"film-title"})
            nominations = soup.find_all("td", attrs={"class":"film-nominations"})
            awards = soup.find_all("td", attrs={"class":"film-awards"})
            bests = soup.find_all("td", attrs={"class":"film-best-picture"})

            
            # Save data
            for title, nomination, award, best in zip(titles, nominations, awards, bests):
                # Mark the best picture with "Best"
                # Get all children tags -> Children tags isn't empty = mark of best picture
                if best.find_all(True) != []:
                    best_w = "Best"
                else:
                    best_w = ""

                writer.writerow([year, title.text.strip(), nomination.text.strip(), award.text.strip(), best_w])

        driver.quit()






if __name__ == "__main__":
    main()