"""
Scrapes countries from https://www.scrapethissite.com/pages/simple/ to a csv file.
"""

from bs4 import BeautifulSoup
import requests
import csv


def main():

    # Open csv file to save extracted data
    with open("countries.csv", "w", encoding="utf-8") as file:

        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        # First row (titles)
        writer.writerow(["Country", "Capital", "Population", "Area[km2]"])

        page = requests.get("https://www.scrapethissite.com/pages/simple/")

        soup = BeautifulSoup(page.text, "html.parser")
        # Get the data
        countries = soup.find_all("h3", attrs={"class":"country-name"})
        capitals = soup.find_all("span", attrs={"class":"country-capital"})
        populations = soup.find_all("span", attrs={"class":"country-population"})
        areas = soup.find_all("span", attrs={"class":"country-area"})
        
        # Write the data to the file
        for i in range(len(countries)):
            writer.writerow([countries[i].text.strip(), capitals[i].text, populations[i].text, areas[i].text])








if __name__ == "__main__":
    main()