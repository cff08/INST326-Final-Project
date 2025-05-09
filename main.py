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
from notification_system import send_event_notifications

def main():
    """
    - Scrapes events
    - Stores them in the database
    - Lets a user bookmark/RSVP to events into lists
    """
    # Initialize components
    url = "https://stamp.umd.edu/upcoming_events"
    scraper = EventScraper(url)
    db = EventsFinderDB()
    storage = StorageSystem()
    user_db = UsersFinderDB()
   

    event_list = scraper.scrape_events()
    
    for event in event_list:
        title = event['title']
        date = event['date']
    
        if not db.event_exists(title, date):
            event_id = db.add_events(title, date)
            print(f"Inserted: {title} - {date}")
        
        else:
            print(f"Skipped: {title} already exists")
    
    send_event_notifications(db.conn)
    
    db.close()
    storage.close()
    user_db.close()


   
if __name__ == "__main__":
    main()
