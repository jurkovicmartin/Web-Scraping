"""
Scrapes https://books.toscrape.com to a csv file.
"""

from bs4 import BeautifulSoup
import requests
import csv


def main():
    # Number of pages to scrape
    PAGES_NUMBER = 5

    # Open csv file to save extracted data
    with open("books.csv", "w", encoding="utf-8") as file:
        
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        # First row (titles)
        writer.writerow(["Title", "Price[£]", "Rating[stars]", "In stock", "UPC"])

        for i in range(1, PAGES_NUMBER + 1):
            # Page to scrape
            url = "https://books.toscrape.com/catalogue/" + f"page-{i}.html"
            page = requests.get(url)
            html = page.text

            main_soup = BeautifulSoup(html, "html.parser")

            # Each div contains one book
            quotes_divisions = main_soup.find_all("li", attrs={"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})

            for div in quotes_divisions:
                
                ### INFO FROM MAIN PAGE

                title = div.find("h3")

                price = div.find("p", attrs={"class":"price_color"})
                # Get only numbers
                price = price.text[2:]

                stock = div.find("p", attrs={"class":"instock availability"})
                if stock.text.strip() == "In stock":
                    stock = "Yes"
                else:
                    stock = "No"

                # Get the <p></p> where the rating is
                rating = div.find("p")
                # Get the class (different rating has different class)
                rating = rating.get("class")[1]
                # Convert rating to number
                rating = convert_rating(rating)


                ### INFO FROM DETAIL PAGE

                # Get link to the book info
                link = div.find("a")
                link = link.get("href")

                page = requests.get("https://books.toscrape.com/catalogue/" + link)
                side_soup = BeautifulSoup(page.text, "html.parser")

                upc = side_soup.find("td")


                # Writing the extracted data
                writer.writerow([title.text, price, rating, stock, upc.text])



def convert_rating(rating: str) -> int:
    """
    Converts rating from word to number.

    Returns -1 when rating isn't valid (else that 0-5).
    """
    if rating == "Zero":
        return 0
    elif rating == "One":
        return 1
    elif rating == "Two":
        return 2
    elif rating == "Three":
        return 3
    elif rating == "Four":
        return 4
    elif rating == "Five":
        return 5
    else:
        # Not valid rating
        return -1

if __name__ == "__main__":
    main()