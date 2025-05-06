import smtplib
import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from dateutil import parser as dt_parser

# Email function (Gmail SMTP as an example)
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
            server.sendmail('John1@example.com', [to_email], msg.as_string())
        print(f"[EMAIL] Sent to {to_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send email to {to_email}: {e}")

# Log in-app notifications (this could eventually display in the app)
def log_in_app(user_id, message):
     """Logs an in-app notification for a user.

    Args:
        user_id (int): The user’s ID to whom the notification belongs.
        message (str): The notification message to be logged.

    Returns:
        None """
    print(f"[IN-APP] Notification for user {user_id}: {message}")
    # Log to database or file (example using a simple log)
    with open("app_notifications.log", "a") as log_file:
        log_file.write(f"User {user_id}: {message}\n")

# Main function to send notifications
def send_event_notifications():
    """ Sends email and in-app notifications for upcoming events within the next hour.

    This function fetches events happening today and checks if their start time is 
    within the next hour. If so, it sends email and logs an in-app notification 
    to the users who favorited the event.

    Args:
        None

    Returns:
        None """
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)
    today_str = now.strftime("%Y-%m-%d")

    cursor.execute("SELECT id, event_name, event_time FROM events WHERE event_date = ?", (today_str,))
    events = cursor.fetchall()

    for event_id, name, time_str in events:
        start_time_str = time_str.split("-")[0].strip()  # Extract the start time
        full_time_str = f"{today_str} {start_time_str}"

        try:
            event_start_dt = dt_parser.parse(full_time_str)
        except Exception as e:
            print(f"Could not parse time for event '{name}': {e}")
            continue

        if now <= event_start_dt <= one_hour_later:
            cursor.execute("SELECT user_id FROM favorites WHERE event_id = ?", (event_id,))
            users = cursor.fetchall()

            for (user_id,) in users:
                email = f"{user_id}@terpmail.umd.edu"  # Example email
                msg = f"Reminder: '{name}' starts at {start_time_str}."

                # Send email notification
                send_email(email, "Event Reminder", msg)

                # Log in-app notification
                log_in_app(user_id, msg)

    conn.close()

if __name__ == "__main__":
    send_event_notifications()
