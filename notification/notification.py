"""Provides notifications for upcoming campus events in the UMD Event App.
Can Handle: 
-registering users with preferences 
- adding new events to the system 
- sending timely notifications based on user interests and event timing"""

class Event: 
    """Represents a campus event. 
    Attributes: 
        title(str): The name of the event 
        category(str): The category such as sports, music, cultural, etc.
        location (str): where the event is happening 
        time (datetime): the date and time of event """
    def __init__(self, title, category, location, time):
        self.title = title
        self.category = category
        self.location = location
        self.time = time 

class NotificationSystem: 
    def __init__(self): 
        """Initialize the lists to store user and events.
        
        Args: 
        
        Returns: 
        """
        self.users = []
        self.events = []

    def user_registration(self,user): 
        """Registers a new user to receive notifications.
       
        Args: 
            user (User): A user object that has preferences and notification settings.

        Returns: 

        """
        self.users.append(user)

    def add_event(self, event): 
        """Adds a new event to the system. 
        
        Args: 
            event (Event): An Event object with title, category, location, and time.
            
        Returns: 
        """
        self.events.append(event)

    def notification_delivery(self, current_time): 
        """Sends notifications to users whose interests match upcoming evens within their preferences
        such as preferred time window.
        
        Args: 
            current_time (datetime): The current time used to calculate time until each event.
        
        Returns: 

        """
        pass

    def _notify(self, user, event): 
        """Internal methods used to simulate notifying a user. 
        
        Args: 
            user(User): the user to notify.
            event(Event): the event that matches the user's interests.
            
        Returns: 
        """
        #print statement
        pass 