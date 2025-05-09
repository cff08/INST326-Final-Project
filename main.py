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
from notification_system import NotificationSystem
from datetime import datetime

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
    notifier = NotificationSystem(db.conn)

    email = input("Enter your email: ").strip().lower()
    user_id = user_db.get_user(email)

    if user_id is None:
        choice = input("User not found. Would you like to register? (yes/no): ").strip().lower()
        if choice == "yes":
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            user_id = user_db.add_user(username, email, password)
            if user_id is None:
                print("Registration failed.")
                return
        else:
            print("Exiting. You must be registered to continue.")
            return

    event_list = scraper.scrape_events()

    for event in event_list:
        title = event['title']
        date = event['date']
        if not db.event_exists(title, date):
            db.add_events(title,date)

    print("\n ----------- EVENTS HAPPENING TODAY ------------")
    cursor = db.conn.cursor()
    cursor.execute("SELECT id, event_name, event_date FROM events")
    events = cursor.fetchall()
    tdevents = []

    # Step 4: Run notification system
    for event_id, name, date in events:
        if notifier.is_event_td(date):
            tdevents.append((event_id, name, date))
            print(f"[{event_id}] {name} - {date}")

    if not tdevents:
        print("No events today")
    else:
       response = input("Would you like to favorite any of these events? (yes/no): ").strip().lower()
       
       if response == "yes":
            selected = input("Enter the ID(s) of the events to favorite (comma-separated): ")
            
            selected_ids = []
            for x in selected.split(","):
                x = x.strip()
                if x.isdigit():
                    selected_ids.append(int(x))
            
            for event_id in selected_ids:
                success = storage.add_bookmark(user_id, event_id)
                if success:
                    print(f"Event {event_id} favorited.")
                else:
                    print(f"Event {event_id} already favorited.")


    # Cleanup
    db.close()
    storage.close()
    user_db.close()

if __name__ == "__main__":
    main()

    
    # for event in event_list:
    #     title = event['title']
    #     date = event['date']
    
    #     if not db.event_exists(title, date):
    #         event_id = db.add_events(title, date)
    #         print(f"Inserted: {title} - {date}")
        
    #     else:
    #         print(f"Skipped: {title} already exists")
    
    # send_event_notifications(db.conn)
    
    # db.close()
    # storage.close()
    # user_db.close()


   
