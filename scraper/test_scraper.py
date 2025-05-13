import unittest
from scraper.scraper import EventScraper

class TestEventScraper(unittest.TestCase):
    """
    Unit tests for the EventScraper class to verify that event data is being fetched and structured correctly.
    """

    def setUp(self):
        """
        Set up the scraper instance with the STAMP events URL before each test.
        """
        self.url = "https://stamp.umd.edu/upcoming_events"
        self.scraper = EventScraper(self.url)

    def test_fetch_page(self):
        """
        Test that the get_soup() method returns a non-None BeautifulSoup object when the page loads successfully.
        """
        soup = self.scraper.get_soup()
        self.assertIsNotNone(soup)

    def test_scrape_events_returns_list(self):
        """
        Test that scrape_events() returns a list and that each dictionary in the list contains 'title' and 'date' keys.
        """
        events = self.scraper.scrape_events()
        self.assertIsInstance(events, list)
        if events: 
            self.assertIn("title", events[0])
            self.assertIn("date", events[0])

    def test_event_data_fields(self):
        """
        Test that the 'title' and 'date' fields in each event are strings.
        """
        events = self.scraper.scrape_events()
        for event in events:
            self.assertIsInstance(event["title"], str)
            self.assertIsInstance(event["date"], str)

if __name__ == "__main__":
    unittest.main()