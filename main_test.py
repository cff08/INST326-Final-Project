import unittest
from unittest.mock import patch, MagicMock
import main

class TestMain(unittest.TestCase):

    @patch("main.NotificationSystem")
    @patch("main.UsersFinderDB")
    @patch("main.StorageSystem")
    @patch("main.EventsFinderDB")
    @patch("main.EventScraper")

    def test_main(self, scraper, eventsdb, storage, userdb, notification):
        
        event_lists = [{"title": "Event 1", "date": "2025-05-09"},
                       {"title": "Event 2", "date": "2025-05-10"}]
        
        scraper = scraper.return_value
        scraper.scrape_events.return_value = event_lists

        db = eventsdb.return_value
        db.event_exists.side_effect = [False, True]
        db.add_events.return_value = ""
        db.conn = "connection"

        main.main()

        scraper.scrape_events.assert_called_once()

        db.event_exists.assert_any_call("Event 1", "2025-05-09")
        db.event_exists.assert_any_call("Event 2", "2025-05-10")
        db.add_events.assert_called_once_with("Event 1", "2025-05-09")

        notification.assert_called_once_with("connection")

        db.close.assert_called_once()
        storage.return_value.close.assert_called_once()
        userdb.return_value.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()




   