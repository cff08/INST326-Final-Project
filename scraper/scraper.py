"""
Scrapes upcoming UMD events from the Stamp website.

This script defines the EventScraper class, which uses requests and BeautifulSoup
to fetch and parse events from the Stamp event calendar. When run directly, it
stores new events in the SQLite database using EventsFinderDB.
"""

import requests
from bs4 import BeautifulSoup
from database.event_database import EventsFinderDB

class EventScraper:
    """Handles scraping of event data from a specified URL."""
    def __init__(self, url):
        """Initializes the scraper with the URL to scrape.

        Args:
            url (str): The webpage URL to fetch event data from.
        """
        self.url = url

    def get_soup(self):
        """Fetches the HTML content from the URL and parses it with BeautifulSoup.

        Returns:
            BeautifulSoup or None: Parsed HTML soup if successful, otherwise None. 
            Prints status message in terminal
        """
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
        """Extracts event titles and dates from the Stamp event page.

        Returns:
            list of dict: A list of events, each represented as a dictionary with 'title' and 'date' keys. 
            Prints the number of events found and any scraping status messages.
        """
        soup = self.get_soup()
        events = []

        if soup is not None:
            cards = soup.find_all('div', class_= 'card-body')
            print(f"Found {len(cards)} events on this page.")

            # Loop through all event cards to extract title and date
            for card in cards:
                title = "No Title"
                date_tag = card.find('div', class_='profile-card-title')

                title_tag = card.find('h2', class_ = 'card-title')
                if title_tag is not None:
                    title = title_tag.get_text(strip=True)

                date_tag = card.find('div', class_='profile-card-title')
                if date_tag is not None:
                    date = date_tag.get_text(strip=True)

                # Create dictionary of scraped event information
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

    db = EventsFinderDB()

    for event in event_list:
        title = event['title']
        date = event['date']

        if not db.event_exists(title, date):
            event_id = db.add_events(title, date)
            print(f"Inserted into DB: {title} on {date} (event_id={event_id})")
        else:
            print(f"[SKIPPED] '{title}' on {date} already exists.")

    db.close()

    # for event in event_list:
    #     print(f"Title: {event['title']}")
    #     print(f"Date: {event['date']}")
    #     print("-" * 50)