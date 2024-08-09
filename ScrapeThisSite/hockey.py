"""
Scrapes hockey teams from https://www.scrapethissite.com/pages/forms/ to a csv file.
"""

from bs4 import BeautifulSoup
import requests
import csv


def main():

    # Open csv file to save extracted data
    with open("hockey.csv", "w", encoding="utf-8") as file:

        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        # First row (titles)
        titles = [
            "Name",
            "Year",
            "Wins",
            "Losses",
            "OT losses",
            "Win %",
            "Goals For",
            "Goals Against"
            "Goals difference"
        ]
        writer.writerow(titles)

        # Number of pages to scrape
        PAGES_NUMBER = 10

        for i in range(1, PAGES_NUMBER + 1):
            url = "https://www.scrapethissite.com/pages/forms/?page_num=" + f"{i}"

            page = requests.get(url)

            soup = BeautifulSoup(page.text, "html.parser")
            # Get the data
            names = soup.find_all("td", attrs={"class":"name"})
            years = soup.find_all("td", attrs={"class":"year"})
            wins = soup.find_all("td", attrs={"class":"wins"})
            losses = soup.find_all("td", attrs={"class":"losses"})
            ot_losses = soup.find_all("td", attrs={"class":"ot-losses"})
            wins_percent = soup.find_all("td", attrs={"class":"pct"})
            goals_for = soup.find_all("td", attrs={"class":"gf"})
            goals_again = soup.find_all("td", attrs={"class":"ga"})
            goals_diff = soup.find_all("td", attrs={"class":"diff"})
            
            
            # Write the data to the file
            for name, year, win, lose, ot_lose, win_percent, goal_for, goal_again, goal_diff in zip(names, years, wins, losses, ot_losses, wins_percent, goals_for, goals_again, goals_diff):
                # Rewrite empty strings with 0
                if ot_lose.text.strip() == "":
                    ot_lose_w = "0"
                else:
                    ot_lose_w = ot_lose.text.strip()
                    
                writer.writerow([name.text.strip(), year.text.strip(), win.text.strip(), lose.text.strip(), ot_lose_w, win_percent.text.strip(), goal_for.text.strip(), goal_again.text.strip(), goal_diff.text.strip()])








if __name__ == "__main__":
    main()