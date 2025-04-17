#INST326: Final Project
#Event Finder App


DATABASE_NAME = "...."

class Database:
    """
    Manage user information and event creation.
    """
    def __init__(self, database_name):
        self.cursor.execute("CREATE DATABASE...")
        pass

    def create_table(self):
        self.cursor.execute("CREATE TABLE...")
        pass

    def add_user(self):
        """Add a new user
    
        Args:
            name(str): Name of the user
            email_add(str): Email address of the user
            password(str): Password of the user
        """
        self.cursor.execute("INSERT INTO users...")
        pass


    def add_events(self): 
        """
        Add a new event

        Args:
            event_name(str): The name of the event
            event_details(str): Details of the event
            category(str): List of event category
            location(str): The location of the event
            start_time(datetime): Start time of the event
            end_time(datetime): End time of the event
        """
        self.cursor.execute("INSERT INTO events...")
        pass

    def update_event(self):
        """
        Update event if there any changes.

         Args:
            event_name(str): The name of the event
            event_details(str): Details of the event
            category(str): List of event category
            location(str): The location of the event
            start_time(datetime): Start time of the event
            end_time(datetime): End time of the event
        """
        self.cursor.execute("UPDATE events SET...")
        pass