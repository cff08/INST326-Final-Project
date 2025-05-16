import sqlite3

class StorageSystem:
    """
    The storage system for the UMD Event App.
    - manages user data storage for the UMD Event App using SQLite
    - handles creation and interaction with 'favorites' and 'rsvps' tables """

    def __init__(self, database_name="events.db"):
        """
        Initializes the storage system
        Args: database_name (str): The name of the SQLite database file
        
        Returns: None
        """
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_favorites_table()
        self.create_rsvp_table()

    def create_favorites_table(self):
        """
        Creates the favorites table if it doesn't exist """

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                event_id INTEGER,
                PRIMARY KEY (user_id, event_id)
            )
        ''')
        self.conn.commit()

    def create_rsvp_table(self):
        """ Creates the RSVPs table for storing user RSVPs  """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rsvps (
                user_id INTEGER,
                event_id INTEGER,
                PRIMARY KEY (user_id, event_id)
            )
        ''')
        self.conn.commit()

    # ---------- BOOKMARKS / FAVORITES ----------
    def add_bookmark(self, user_id, event_id):
        """ adds a boomark to the favorites table 
        Args:
            user_id (int): The ID of the user
            event_id (int): The ID of the event
        
        Returns: boolean
            True if the bookmark was added successfully, False otherwise
        """
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO favorites (user_id, event_id) VALUES (?, ?)",
                (user_id, event_id)
            )
            self.conn.commit()
            return True
        except:
            return False

    def remove_bookmark(self, user_id, event_id):

        """ removes a bookmark from the favorites table
         Args:
            user_id (int): The ID of the user
            event_id (int): The ID of the event
        Returns:
            None
        """
        self.cursor.execute(
            "DELETE FROM favorites WHERE user_id = ? AND event_id = ?",
            (user_id, event_id)
        )
        self.conn.commit()

    def get_user_bookmarks(self, user_id):

        """ retrieves all bookmarks for a user
        Args:
            user_id (int): The ID of the user
        Returns:
            A list of tuples containing event details (event_id, event_name, event_date, location, event_time)
        """

        self.cursor.execute('''
            SELECT e.id, e.event_name, e.event_date, e.location, e.event_time
            FROM events e
            JOIN favorites f ON e.id = f.event_id
            WHERE f.user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    # ---------- RSVPS ----------
    def add_rsvp(self, user_id, event_id):
        """ adds an RSVP to the RSVPs table
        Args:
            user_id (int): The ID of the user
            event_id (int): The ID of the event
        Returns:
            True if the RSVP was added successfully, False otherwise
        """
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO rsvps (user_id, event_id) VALUES (?, ?)",
                (user_id, event_id)
            )
            self.conn.commit()
            return True
        except:
            return False

    def cancel_rsvp(self, user_id, event_id):
        """ removes an RSVP from the RSVPs table
        Args:
            user_id (int): The ID of the user
            event_id (int): The ID of the event
        Returns:
            None
        """
        self.cursor.execute(
            "DELETE FROM rsvps WHERE user_id = ? AND event_id = ?",
            (user_id, event_id)
        )
        self.conn.commit()

    def get_user_rsvps(self, user_id):
        """ retrieves all RSVPs for a user
        Args:
            user_id (int): The ID of the user
        Returns:
            A list of tuples containing event details (event_id, event_name, event_date, location, event_time)
        """
        self.cursor.execute('''
            SELECT e.id, e.event_name, e.event_date, e.location, e.event_time
            FROM events e
            JOIN rsvps r ON e.id = r.event_id
            WHERE r.user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    s = StorageSystem()
    s.close()
    print("Favorites and RSVPs tables created.")