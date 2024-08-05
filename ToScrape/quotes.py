"""
Scrapes quote, author and tags to a csv file from http://quotes.toscrape.com site.
"""

from bs4 import BeautifulSoup
import requests
import csv


def main():
    # Number of pages to scrape
    PAGES_NUMBER = 5

    # Open csv file to save extracted data
    with open("quotes.csv", "w") as file:
        
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        # First row (titles)
        writer.writerow(["Quote", "Author", "Tags"])

        for i in range(1, PAGES_NUMBER + 1):
            # Page to scrape
            url = "http://quotes.toscrape.com/page/" + f"{i}/"
            page = requests.get(url)
            html = page.text

            soup = BeautifulSoup(html, "html.parser")

            # Each div contains one quote
            quotes_divisions = soup.find_all("div", attrs={"class":"quote"})

            for div in quotes_divisions:
                # Only one quote and author
                quote = div.find("span", attrs={"class":"text"})
                author = div.find("small", attrs={"class":"author"})
                # Multiple tags
                tags = div.find_all("a", attrs={"class":"tag"})
                # Get only the text
                tags = [tag.text for tag in tags]

                # Writing the extracted data
                writer.writerow([quote.text, author.text, ", ".join(tags)])

   


if __name__ == "__main__":
    main()