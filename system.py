"""
Manages storage-related user interactions in the UMD Event App.
Responsible for:
- RSVPing/Bookmarking events
- Removing RSVPs/Bookmarks
- Storing user preferences

"""

class StorageSystem:
    def __init__(self):
        """
    
        creates a list to store user bookmarks and RSVPS

        ARGS: 

        Returns:

        """
        self.bookmarks = []
        self.rsvps = []

    def bookmark_event(self, event_name):
        """
        Bookmarks an event for the user

        Args:
            event_name: the specific ID of the event to bookmark

        Returns:
            True to appending new even_id to the bookmarks list, and false if the event is already bookmarked.
        """
        pass

    def rsvp_event(self, event_name):
        """
        RSVP to an event.

        Args:
            event_name (str): The unique ID of the event.

        Returns:
            bool: True if RSVP successful, False if already RSVP’d.
        """
        pass
    def remove_bookmark(self, event_name):
        """
        Removes an event from the user's bookmarked list.

        Args:
            event_name (str): name of event to remove.

        Returns:
            bool: True if removal successful, False if event not found in bookmarks.
            Displays all bookmarks after removal
        """
        pass
    def cancel_rsvp(self, event_name):
        """Removes an event from the user's RSVP list.
    
        Args:
            event_name (str): name of event to remove.
            Returns: 
            bool: True if removal successful, False if event not found in RSVPs.
            """
        pass

    def display_bookmarks(self):
        """
        Displays all bookmarked events.

        Returns:
            list: A list of all bookmarked event names.
        """
        return self.bookmarks

    def display_rsvps(self):
        """
        Displays all RSVPed events.

        Returns:
            list: A list of all RSVPed event names.
        """
        return self.rsvps
    