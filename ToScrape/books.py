"""
Scrapes https://books.toscrape.com to a csv file.
"""

from bs4 import BeautifulSoup
import requests
import csv


def main():
    # Number of pages to scrape
    PAGES_NUMBER = 1

    # Open csv file to save extracted data
    with open("books.csv", "w", encoding="utf-8") as file:
        
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        # First row (titles)
        writer.writerow(["Title", "Price[£]", "In stock"])

        for i in range(1, PAGES_NUMBER + 1):
            # Page to scrape
            url = "https://books.toscrape.com/catalogue/" + f"page-{i}.html"
            page = requests.get(url)
            html = page.text

            soup = BeautifulSoup(html, "html.parser")

            # Each div contains one book
            quotes_divisions = soup.find_all("li", attrs={"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})

            for div in quotes_divisions:
                title = div.find("h3")
                price = div.find("p", attrs={"class":"price_color"})
                # Get only numbers
                price = price.text[2:]
                stock = div.find("p", attrs={"class":"instock availability"})

                if stock.text.strip() == "In stock":
                    stock = "Yes"
                else:
                    stock = "No"

                # Writing the extracted data
                writer.writerow([title.text, price, stock])

   


if __name__ == "__main__":
    main()