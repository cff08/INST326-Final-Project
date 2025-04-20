class EventScraper:
    """
    A web scraper for extracting event information from a UMD events page.
    """

    def __init__(self, url: str):
        """
        Initializes the scraper with a specific URL.
        
        Args:
            url (str): The URL of the page to scrape.
        """
        pass

    def fetch_page(self):
        """
        Fetches HTML content from the target URL and prepares it for parsing.
        """
        pass

    def parse_events(self):
        """
        Parses the fetched HTML and extracts event data including title, date, and location.

        Returns:
            list[dict[str, str]]: A list of events with key details.
        """
        pass

    def scrape(self):
        """
        Executes the full scraping process from fetching to parsing.

        Returns:
            list[dict[str, str]]: A list of event dictionaries from the source.
        """
        pass
