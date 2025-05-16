import unittest
import sqlite3
from system.system import StorageSystem
"""
Unit tests for the storage system class.
- Adding/removing event bookmarks for a user.
- Adding/cancelling RSVPs for a user.
"""
class TestStorageSystem(unittest.TestCase):
    """ 
    Unit tests for the StorageSystem class
    - Tests the functionality of creating tables, adding/removing bookmarks and RSVPs
    """
    def setUp(self):
 
        self.storage = StorageSystem(":memory:")

        self.storage.cursor.execute('''
            CREATE TABLE events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT,
                event_date TEXT,
                location TEXT,
                event_time TEXT
            )
        ''')

        self.storage.cursor.execute('''
            INSERT INTO events (event_name, event_date, location, event_time)
            VALUES ("Test Event", "2025-05-10", "UMD Campus", "5:00PM")
        ''')
        self.storage.conn.commit()

        self.user_id = 1
        self.event_id = 1  

    def tearDown(self):
        """
        Closes the connection to the in-memory database after each test.
        """
        self.storage.close()

    def test_add_bookmark(self):
        """ 
        adds a bookmark to the favorites table
        Args:
            user_id (int): The ID of the user
            event_id (int): The ID of the event


        """
        result = self.storage.add_bookmark(self.user_id, self.event_id)
        self.assertTrue(result)

        bookmarks = self.storage.get_user_bookmarks(self.user_id)
        self.assertEqual(len(bookmarks), 1)
        self.assertEqual(bookmarks[0][0], self.event_id)

    def test_remove_bookmark(self):
        """
        adds a bookmark and then removes a bookmark from the favorites table
        Args:
            user_id (int): The ID of the user
            event_id (int): The ID of the event
        """
        self.storage.add_bookmark(self.user_id, self.event_id)
        self.storage.remove_bookmark(self.user_id, self.event_id)

        bookmarks = self.storage.get_user_bookmarks(self.user_id)
        self.assertEqual(len(bookmarks), 0)

    def test_add_rsvp(self):
        """
        adds a RSVP to the RSVPs table
        Args:
            user_id (int): The ID of the user
            event_id (int): The ID of the event
        """
        result = self.storage.add_rsvp(self.user_id, self.event_id)
        self.assertTrue(result)

        rsvps = self.storage.get_user_rsvps(self.user_id)
        self.assertEqual(len(rsvps), 1)
        self.assertEqual(rsvps[0][0], self.event_id)

    def test_cancel_rsvp(self):
        """
        adds a RSVP and then cancels a RSVP from the RSVPs table
        Args:
            user_id (int): The ID of the user
            event_id (int): The ID of the event
        """
        self.storage.add_rsvp(self.user_id, self.event_id)
        self.storage.cancel_rsvp(self.user_id, self.event_id)

        rsvps = self.storage.get_user_rsvps(self.user_id)
        self.assertEqual(len(rsvps), 0)


if __name__ == '__main__':
    unittest.main()
