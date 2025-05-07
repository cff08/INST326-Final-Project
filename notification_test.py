import unittest
from unittest.mock import patch
from notification_system import send_email,log_in_app  
from event_database import EventsFinderDB
from user_database import UsersFinderDB

class TestNotification(unittest.TestCase):
    def setUp(self):
        self.event_db = EventsFinderDB(":memory:")  # Using an in-memory database for testing
        self.user_db = UsersFinderDB(":memory:")    # Using an in-memory database for testing

        # Add mock user to the database for testing
        self.user_db.add_user("John", "john@example.com", "password123")
        self.event_db.add_events("Test Event", "2025-05-10", "HBK", "3:00pm - 4:00pm")

    def tearDown(self):
        self.event_db.close()
        self.user_db.close()

    @patch("notification_system.send_email")
    @patch("notification_system.log_in_app")
    def test_send_event_notifications(self, mock_log_in_app, mock_send_email):
        # Simulate the event notifications process
        self.event_db.send_event_notifications()  # Assuming this is your function to trigger notifications
        
        # Check that the email function was called with the correct arguments
        mock_send_email.assert_called_with("john@example.com", "Event Reminder", "Reminder: 'Test Event' starts at 3:00pm.")
      
        # Check that the in-app notification function was called with the correct arguments
        mock_log_in_app.assert_called_with(1, "Reminder: 'Test Event' starts at 3:00pm.")  # Assuming user ID is 1

if __name__ == "__main__":
    unittest.main()
