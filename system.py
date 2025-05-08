import sqlite3

"""
Manages storage-related user interactions in the UMD Event App.
Responsible for:
- RSVPing/Bookmarking events
- Removing RSVPs/Bookmarks
- Storing user preferences

"""
class StorageSystem:
    def __init__(self, database_name="events.db"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_favorites_table()
        self.create_rsvp_table()

    def create_favorites_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                event_id INTEGER,
                PRIMARY KEY (user_id, event_id)
            )
        ''')
        self.conn.commit()

    def create_rsvp_table(self):
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
        self.cursor.execute(
            "DELETE FROM favorites WHERE user_id = ? AND event_id = ?",
            (user_id, event_id)
        )
        self.conn.commit()

    def get_user_bookmarks(self, user_id):
        self.cursor.execute('''
            SELECT e.id, e.event_name, e.event_date, e.location, e.event_time
            FROM events e
            JOIN favorites f ON e.id = f.event_id
            WHERE f.user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    # ---------- RSVPS ----------
    def add_rsvp(self, user_id, event_id):
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
        self.cursor.execute(
            "DELETE FROM rsvps WHERE user_id = ? AND event_id = ?",
            (user_id, event_id)
        )
        self.conn.commit()

    def get_user_rsvps(self, user_id):
        self.cursor.execute('''
            SELECT e.id, e.event_name, e.event_date, e.location, e.event_time
            FROM events e
            JOIN rsvps r ON e.id = r.event_id
            WHERE r.user_id = ?
        ''', (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()