import unittest
from event_database import EventsFinderDB
from user_database import UsersFinderDB

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.db = EventsFinderDB(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_event(self):
        self.db.add_events("School Event", "2025-04-10") 

class TestUser(unittest.TestCase):
    def setUp(self):
        self.db = UsersFinderDB(":memory:")

    def tearDown(self):
        self.db.close()  

    def test_add_user(self):
        self.db.add_user("John", "john@example.com", "123456789")      

if __name__ == "__main__":
    unittest.main()