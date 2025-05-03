import requests
from bs4 import BeautifulSoup
import pandas as pd

class EventScraper:
    def __init__(self, url):
        self.url = url

    def get_soup(self):
        print(f"Fetching page: {self.url}")
        output = requests.get(self.url)

        if output.status_code == 200:
            print("Page fetched")
            soup = BeautifulSoup(output.text, "html.parser")
            return soup
        else:
            print(f"Fetching page failed. Status code: {output.status_code}")
            return None
        
    def scrape_events(self):

        soup = self.get_soup()
        events = []

        if soup is not None:
            cards = soup.find_all('div', class_= 'card-body')
            print(f"Found {len(cards)} events on this page.")

            for card in cards:
                title = "No Title"
                subtitle = "No Subtitle"
                link = "No Link"

                title_tag = card.find('h2', class_ = 'card-title')
                if title_tag is not None:
                    title = title_tag.get_text(strip=True)

                date_tag = card.find('div', class_='profile-card-title')
                if date_tag is not None:
                    date = date_tag.get_text(strip=True)


                event_info = {
                    "title": title,
                    "date": date,
                }
                events.append(event_info)

        else:
            print("Soup object is None. Cannot scrape events.")

        return events
    

if __name__ == "__main__":
    url = "https://stamp.umd.edu/upcoming_events"

    scraper = EventScraper(url)

    event_list = scraper.scrape_events()

    for event in event_list:
        print(f"Title: {event['title']}")
        print(f"Date: {event['date']}")
        print("-" * 50)
