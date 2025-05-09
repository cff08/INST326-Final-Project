import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from notification_system import NotificationSystem
from event_database import EventsFinderDB
from user_database import UsersFinderDB

class TestNotification(unittest.TestCase):
    def setUp(self):
        self.event_db = EventsFinderDB(":memory:")  # Using an in-memory database for testing
        self.user_db = UsersFinderDB(":memory:")    # Using an in-memory database for testing

        # Add mock user to the database for testing
        self.user_db.add_user("John", "john@example.com", "password123")

        # Set test event to start within the next hour 
        now = datetime.now()
        today = now.strftime("%B %d")
        
        event_id = self.event_db.add_events("Test Event", today)
        self.event_db.add_favorite(1, event_id)
        
    def tearDown(self):
        self.event_db.close()
        self.user_db.close()

    @patch.object(NotificationSystem, "send_email")
    @patch.object(NotificationSystem, "log_in_app")

    def test_send_event_notifications(self, mock_log_in_app, mock_send_email):
        notifier = NotificationSystem(self.event_db.conn)
        notifier.send_event_notifications()

        expected_msg = "Reminder: 'Test Event' is happening today!"
        mock_send_email.assert_called_with("1@terpmail.umd.edu", "Event Reminder", expected_msg)
        mock_log_in_app.assert_called_with(1, expected_msg)


if __name__ == "__main__":
    unittest.main()
