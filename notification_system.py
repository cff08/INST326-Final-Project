import smtplib
import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from dateutil import parser as dt_parser

# Email function 
def send_email(to_email, subject, body):
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
        print(f"[EMAIL SENT] To {to_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email to {to_email}: {e}")

# Log in-app notifications 
def log_in_app(user_id, message):
    """Logs an in-app notification for a user.

    Args:
        user_id (int): The user’s ID to whom the notification belongs.
        message (str): The notification message to be logged.

    Returns:
        None """
    print(f"[IN-APP] Notification for user {user_id}: {message}")
    try:
    # Log to database or file 
        with open("app_notifications.log", "a") as log_file:
            log_file.write(f"User {user_id}: {message}\n")
    except Exception as e: 
        print(f"[LOG ERROR] Could not write to log file: {e}")

# Main function to send notifications
def send_event_notifications(conn):
    cursor = conn.cursor()

    now = datetime.now()
    today_str = now.strftime("%B %d").lower()     # "May 09"
    today_day = now.strftime("%A").lower()        # "friday"

    print(f"Checking for events occurring on {today_str} ({today_day})")

    cursor.execute("SELECT id, event_name, event_date FROM events")
    events = cursor.fetchall()

    matches_today = 0

    for event_id, name, event_date in events:
        event_date = event_date.lower()
        matched = False

        #Checking for date in range format.
        event_date = event_date.replace("—", " to ").replace("–", " to ")

        if " to " in event_date:
            date_range = event_date.split(" to ")
            
            if len(date_range) == 2:
                start_str = date_range[0].strip()
                end_str = date_range[1].strip()

                try:
                    start_date = datetime.strptime(start_str, "%B %d").replace(year=now.year)
                    end_date = datetime.strptime(end_str, "%B %d").replace(year=now.year)

                    if start_date <= now <= end_date:
                        matched = True

                except ValueError as e:
                    print(f"[PARSE ERROR] Could not parse date range for '{name}': {event_date}")


        #Direct match for today’s date (e.g., “may 9” in “Wednesday, May 9”)
        if not matched and today_str in event_date:
            matched = True

        #Day-of-week keywords (like “Fridays”)
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in weekdays:
            if day in event_date or day + "s" in event_date:
                if day == today_day:
                    matched = True

        if matched:
            matches_today += 1
            cursor.execute("SELECT user_id FROM favorites WHERE event_id = ?", (event_id,))
            users = cursor.fetchall()

            if not users:
                print(f"No users favorited event '{name}'")
            else:
                for (user_id,) in users:
                    email = f"{user_id}@terpmail.umd.edu"
                    msg = f"Reminder: '{name}' is happening today!"
                    send_email(email, "Event Reminder", msg)
                    log_in_app(user_id, msg)

    if matches_today == 0:
        print("No events happening today.")
    else:
        print(f"Found {matches_today} event(s) happening today.")

    conn.close()
if __name__ == "__main__":
    conn = sqlite3.connect("events.db")
    send_event_notifications(conn)
    conn.close()
    
