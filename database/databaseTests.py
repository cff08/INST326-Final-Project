import unittest
from event_database import EventsFinderDB
from user_database import UsersFinderDB
"""
Unit tests for the EventsFinderDB and UsersFinderDB database.
"""
class TestEvent(unittest.TestCase):
    """
    - Adding events to memory EventsFinderDB database.
    - Tests the event related methods in EventsFinderDB.
    """
    def setUp(self):
        self.db = EventsFinderDB(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_event(self):
        self.db.add_events("School Event", "2025-04-10") 

class TestUser(unittest.TestCase):
    """
    - Adding user to memory UsersFinderDB database.
    - Tests the event related methods in UsersFinderDB.
    """
    def setUp(self):
        self.db = UsersFinderDB(":memory:")

    def tearDown(self):
        self.db.close()  

    def test_add_user(self):
        self.db.add_user("John", "john@example.com", "123456789")      

if __name__ == "__main__":
    unittest.main()
