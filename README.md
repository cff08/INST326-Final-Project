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


