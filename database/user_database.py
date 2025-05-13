import sqlite3
from datetime import datetime

class UsersFinderDB:
    """
    Manage user information in SQLite database, provides to methods
    to add, update, and remove users.
    """
    def __init__(self, database_name="users.db"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Create users table in the database.
        """
        self.cursor.execute('''
              CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 email TEXT NOT NULL,
                 password TEXT NOT NULL,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
             )
         ''')    
        self.conn.commit()

    def add_user(self, username, email, password):
        """Add a new user.

        Args:
            username (str): Name of the user
            email (str): Email address of the user
            password (str): Password of the user
        """
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

        if self.cursor.fetchone():
            print(f"{username} already exists")
            return None
        self.cursor.execute(
                '''INSERT INTO users (username, email, password) VALUES (?, ?, ?)''',
                (username, email, password)
            )
        self.conn.commit()
        print(f"{username} added successfully.")
        return self.cursor.lastrowid

    
    def get_user(self, email):
        """
        Retrieve user id by email address.

        Args:
            email(str): email of the user
        Returns:
            int or None: user id if found, otherwise None
        """
        self.cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            None

    def update_user(self, user_id, username, email=None, password=None):
        """
        Update user if there are any changes.

        Args:
            user_id (int): The ID of the user
            username (str): The name of the user
            email (str): The email address of the user
            password (str): The password of the user
        """
        update = []
        value = []

        if username:
            update.append("username = ?")
            value.append(username)

        if email:
            update.append("email = ?")
            value.append(email)

        if password:
            update.append("password = ?")
            value.append(password)

        
        value.append(user_id)
        sql = f"UPDATE users SET {', '.join(update)} WHERE id = ?"
        self.cursor.execute(sql, value)
        self.conn.commit()
        print(f"User ID {user_id} update successfully.")  

    def remove_user(self, user_id):
        """
        Remove user from the database.

        Args:
            user_id(int): user id to remove
        """
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()   
        print(f"User ID {user_id} remove successfully.")     
            
    def close(self):
        """
        Close database connection.
        """
        self.conn.close()        

if __name__ == "__main__":
    user = UsersFinderDB()

    #Add user
    #user1 = user.add_user("John", "john@example.com", "123456789")
    #print(user1)
    #user.remove_user(user_id=6)
    user.close()
