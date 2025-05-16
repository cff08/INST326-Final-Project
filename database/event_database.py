"""Database interface for storing and managing UMD event data.

This module defines the EventsFinderDB class for interacting with an
SQLite database that stores event information. It supports adding,
updating, deleting, and checking the existence of events.

"""

import sqlite3
from datetime import datetime

class EventsFinderDB:
    """
    Manage user events and favorites using SQLite. Create events/favorites,
    track user favorit events, add/update/remove events.
    """
    def __init__(self, database_name="events.db"):
        """Initializes a database connection and creates the events table.

        Args:
            database_name (str): Name of the database file to connect to.
        """
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Create events table.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                event_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()


    def add_events(self, event_name, event_date):
        """Adds a new event to the database.

        Args:
            event_name (str): The name of the event.
            event_date (str): The date the event takes place.

        Returns:
            int: The ID of the newly inserted event.
        """
        self.cursor.execute(
            '''INSERT INTO events (event_name, event_date)
               VALUES (?, ?)''',
            (event_name, event_date,)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_event(self, event_id, event_name=None, event_date=None):
        """
        Update event if there are any changes.

        Args:
            event_id (int): The ID of the event
            event_name (str): The name of the event
            event_date (str): The date of the event
            
        """
        
        # Dynamically build SQL update query based on which fields are provided
        update = []
        value = []

        if event_name:
            update.append("event_name = ?")
            value.append(event_name)

        if event_date:
            update.append("event_date = ?")
            value.append(event_date)


        
        value.append(event_id)
        sql = f"UPDATE events SET {', '.join(update)} WHERE id = ?"
        self.cursor.execute(sql, value)
        self.conn.commit()

    def remove_event(self, event_id):
        """
        Remove an event from the database.

        Args:
            event_id(int): id of the event to remove
        """
        
        self.cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.conn.commit()
    
    def event_exists(self, name, date):
        """
        Check an event if already exist in the database.

        Args:
            name(str): name of the event
            date(str): date of the event
        """

        self.cursor.execute(
            "SELECT id FROM events WHERE event_name = ? AND event_date = ?", 
            (name, date)
        )
        return self.cursor.fetchone() is not None

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()

if __name__ == "__main__":
    finder = EventsFinderDB()

    # Add event
    # event1 = finder.add_events("InfoSci Connect", "2025-04-10", "HBK", "2:00pm - 4:00pm")
    # print("Event ID:", event1)

    #finder.remove_event(event_id=3)

    finder.close()
