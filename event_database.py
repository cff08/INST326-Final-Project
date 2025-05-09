import sqlite3
from datetime import datetime

class EventsFinderDB:
    """
    Manage user information and event creation.
    """
    def __init__(self, database_name="events.db"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.create_favorites_table()

    def create_table(self):
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                event_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_favorites_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                event_id INTEGER
            )
        ''')
        self.conn.commit()

    def add_favorite(self, user_id, event_id):
        self.cursor.execute(
            "INSERT INTO favorites (user_id, event_id) VALUES (?, ?)",
            (user_id, event_id)
        )
        self.conn.commit()

    def add_events(self, event_name, event_date):
        """
        Add a new event.

        Args:
            event_name (str): The name of the event
            event_date (str): The date of the event
        
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
        self.cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.conn.commit()
    
    def event_exists(self, name, date):
        self.cursor.execute(
            "SELECT id FROM events WHERE event_name = ? AND event_date = ?", 
            (name, date)
        )
        return self.cursor.fetchone() is not None

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    finder = EventsFinderDB()

    # Add event
    # event1 = finder.add_events("InfoSci Connect", "2025-04-10", "HBK", "2:00pm - 4:00pm")
    # print("Event ID:", event1)

    #finder.remove_event(event_id=3)

    finder.close()
