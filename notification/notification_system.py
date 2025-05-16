"""Handles automated event notifications for users.

This module defines the NotificationSystem class, which checks the database
for any events scheduled for today and sends simulated email and in-app
notifications to users who have favorited those events.

"""

import smtplib
import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from dateutil import parser as dt_parser

class NotificationSystem:
    """Initialize the NotiifcationSystem with a databse connection.
        
        Args: 
            conn(sqlite3.Connection): The SQLite database connection.
    """
    def __init__(self,conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.now = datetime.now() # Current date and time
        self.today_str = self.now.strftime("%B %d").lower() # Today's date in 'Month' day format
        self.today_day = self.now.strftime("%A").lower() # Today's day of the week
        
    # Email function 
    def send_email(self, to_email, subject, body):
        """Sends an email notification using Gmail SMTP.

        Args:
            to_email (str): The recipient's email address.
            subject (str): The subject line of the email.
            body (str): The body content of the email.

        Returns:
            None """
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'John@example.com'  # To be Replaced with real email to send notification from
        msg['To'] = to_email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('John@example.com', 'password')  # Use app password for Gmail
                server.sendmail('John@example.com', [to_email], msg.as_string())
            print(f"To {to_email}")
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")

    # Log in-app notifications 
    def log_in_app(self, user_id, message):
        """Logs an in-app notification for a user.

        Args:
            user_id (int): The user’s ID to whom the notification belongs.
            message (str): The notification message to be logged.

        Returns:
            None """
        print(f"Notification for user {user_id}: {message}")
        try:
        # Log to database or file 
            with open("app_notifications.log", "a") as log_file:
                log_file.write(f"User {user_id}: {message}\n")
        except Exception as e: 
            print(f"Could not write to log file: {e}")

    def is_event_td(self, event_date, name = None):
        """Determine if an event is occuring today based on its date.

        Args: 
            event_date(str): date description of the event.
            name (str, optional): name of the event (for error messages).
        
        Returns:
            bool: True if the event is happening today, or False otherwise. """
            
        event_date = event_date.lower()
        matched = False

        # Normalize date ranges 
        event_date = event_date.replace("—", " to ").replace("–", " to ")

            # Handle date ranges (e.g. "May 1 to May 3")
        if " to " in event_date:
            parts = event_date.split(" to ")
            if len(parts) == 2:
                try:
                    start = datetime.strptime(parts[0].strip(), "%B %d").replace(year=self.now.year)
                    end = datetime.strptime(parts[1].strip(), "%B %d").replace(year=self.now.year)
                    if start <= self.now <= end:
                        matched = True
                except ValueError:
                    print(f"Could not parse date range for '{name}': {event_date}")

            #Direct match for today’s date (e.g., “may 9” in “Wednesday, May 9”)
        if not matched and self.today_str in event_date:
            matched = True

            # 3. Day-of-week match
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in weekdays:
            if (day in event_date or day + "s" in event_date) and day == self.today_day:
                matched = True
        return matched
        
        # Main function to send notifications
    def send_event_notifications(self):
        print(f"Checking for events occurring on {self.today_str} ({self.today_day})")

        self.cursor.execute("SELECT id, event_name, event_date FROM events")
        events = self.cursor.fetchall() #Retrieve all events 

        matches_today = 0

        for event_id, name, event_date in events:
            if self.is_event_td(event_date):
                matches_today += 1
                self.cursor.execute("SELECT user_id FROM favorites WHERE event_id = ?", (event_id,))
                users = self.cursor.fetchall()

                if not users:
                    print(f"No users favorited event '{name}'")
                else:
                    for (user_id,) in users:
                        email = f"{user_id}@terpmail.umd.edu"
                        msg = f"Reminder: '{name}' is happening today!"
                        self.send_email(email, "Event Reminder", msg)
                        self.log_in_app(user_id, msg)
      
        # Display summary of notification results
        if matches_today == 0:
            print("No events happening today.")
        else:
            print(f"Found {matches_today} event(s) happening today.")

        self.conn.close() # Close database connection

if __name__ == "__main__":
    conn = sqlite3.connect("events.db")
    notify = NotificationSystem(conn)
    notify.send_event_notifications()
