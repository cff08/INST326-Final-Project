"""
Entry point for the UMD Event App.
Initializes core backend systems (storage, database, notifications) 

connects backend components together

Planned Responsibilities:
- Interface storage, scraper, and database systems
- combines data interactions with scraped event data
"""

from system import StorageSystem
from event_database import EventsFinderDB
from user_database import UsersFinderDB
from scraper import EventScraper  # assuming this is the class name

def main():
    """
    - Scrapes events
    - Stores them in the database
    - Lets a user bookmark/RSVP to events into lists
    """
    
    # Initialize components
    storage = StorageSystem()
    db = Database()
    scraper = EventScraper()
    notification = NotificationSystem()

   
if __name__ == "__main__":
    main()
