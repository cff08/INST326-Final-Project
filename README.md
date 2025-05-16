# UMD Event Finder App

An interactive command-line application that helps UMD students track on-campus events.

Users can:
- Register with an email and password  
- View real events scraped from the UMD Stamp website  
- Favorite or RSVP to any events happening today  
- Receive simulated reminders for current events  


# Overview

This application is structured around five core modules, each separated into folders for clarity and modularity. The program runs through `main.py`, which guides the user flow and connects all components.


# System Components

## UsersFinderDB
Handles user registration and login using SQLite. Each user is uniquely identified by their email, and their password is stored securely (not in this version). The system prevents duplicate user registration and supports persistent account storage.


## EventsFinderDB
Stores events scraped from the UMD Stamp website. Each event includes a title, date, and creation timestamp. The system prevents duplicate events by checking name–date pairs before insertion.


## StorageSystem
Handles user interactions like favoriting or RSVPing to events. It uses database constraints to prevent duplicate favorites, and supports removing bookmarks or RSVPs if needed. Data is stored persistently in `events.db`.


## EventScraper
Scrapes current event data from [stamp.umd.edu/upcoming_events] using BeautifulSoup. It extracts event titles and dates, and sends them to the database for storage. This runs every time the app is launched to ensure fresh results.


## NotificationSystem
Scans the events database for anything happening today. If matches are found, it simulates email notifications and logs messages to a file. Event date matching is handled by parsing both named days and date ranges like "May 1 — May 21."


# Usage

To run the application:

```bash
python main.py
```
# Outcome
After running python main.py, the terminal should prompt user to enter email. If not registered in system in order to create account with username and password.

Once acount is registered, user will be prompted to viewing event information occuring today from the UMD STAMP events website. Then, users will be asked if they would like to favorite events. They may select event options and will recieve confirmation on the terminal of that event favorited. 

If user already favorited an event before with their account, the terminal will provide a message indicating the event is already favorited. This event will not be repeated in the favorites table. 

# Tech Stack

- Language: Python
- Database: SQLite
- Web Scraping: BeautifulSoup
- Notifications: Console simulation + local log output
- Architecture: Modular folders and imports, with separation across system, database, scraping, and notification components

# Extra/Unused Methods
Some helper methods were developed but not used in the final version of the app. We kept them in the code to reflect our full development process and to support future expansion:

  - update_event() and remove_event() in EventsFinderDB — prepared for manual event editing or removal
  - update_user() and remove_user() in UsersFinderDB — allows future user profile updates or account deletion
  - get_user_bookmarks() and get_user_rsvps() in StorageSystem — could support future user dashboards or analytics
  - send_email() in NotificationSystem — included for simulated email capability, but unused in final CLI flow
  - log_in_app() — logs reminders to a local file; optional for tracking notification history

These unused methods don’t affect functionality and demonstrate the modular, extensible nature of the project.

# Annotated Bibliography


Karajgiker, Jajwalya. “Scraping Open Data from the Web with Beautifulsoup.” Penn Libraries, 17 Dec. 2021, www.library.upenn.edu/rdds/work/beautiful-soup.   
  This source was helpful for guidance in scraping for our project. 
  
Kurweg, Jonas. “How to Set up Mobile App Event Tracking: Complete Guide 2025.” UXCam Blog, 29 Nov. 2024, uxcam.com/blog/mobile-app-event-tracking/.  
  This source gives an overview of why an event tracking app is useful and how it may be implemented.
  
McQuillan, Ronan. “Data Sources for App Projects: Ultimate Guide.” Budibase, Budibase, 9 Aug. 2023, budibase.com/blog/data/data-sources/.  
  This source suggests a way for our project’s database and logging of campus events. 
  
Pal, Himanshu. “Complete Guide on How to Develop Mobile App in Pythoncomplete Guide on How to Develop Mobile App in Python.” IT Services Company in Singapore, 31 Aug. 2023, www.applify.com.sg/blog/how-to-develop-mobile-app-in-python.  
  This is an additional source that provides a detailed step by step guide on how to begin coding for the development of this app. It gives specific criterias to look out for. 
  
“Unittest.Mock - Mock Object Library.” Python Documentation, docs.python.org/3/library/unittest.mock.html.  Accessed 15 May 2025. 
  This document was referred to the unit test portion of our notification system test file. It was particularly helpful in implementing the patch functions. 



