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
    
if __name__ == "__main__":
    url = "https://stamp.umd.edu/upcoming_events"
