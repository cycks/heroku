"""This file contains a class that is used to extract diary contents
from a post request."""
# from datetime import datetime, timedelta

from Users.user_details import UserDetails


class UserEntries(UserDetails):
    """A class used to extract entry details from the post request."""
    def get_title(self):
        """A method used to extract the title from the post request."""
        title = self.details_from_post.get("title", None)
        if self.check_detail_length(title)is True:
            return title
        return False

    def get_contents(self):
        """A method used to extract the contents of an entry from the
         post request"""
        contents = self.details_from_post.get("contents", None)
        if self.check_detail_length(contents)is True:
            return contents
        return False

    def get_date_of_event(self):
        """A method used to extract the date of the event from the
        post request"""
        date_of_event = self.details_from_post.get("date_of_event", None)
        if self.check_detail_length(date_of_event)is True:
            return date_of_event
        return False

    def get_reminder_time(self):
        """A method used to extract the reminder time from the
         post request."""
        reminder_time = self.details_from_post.get("reminder_time", None)
        if self.check_detail_length(reminder_time)is True:
            return reminder_time
        return False

    @property
    def combine_details(self):
        """combines all the entries into a dictionary."""
        check_nulls = {"title": self.get_title(),
                       "contents": self.get_contents(),
                       "date_of_event": self.get_date_of_event(),
                       "reminder_time": self.get_reminder_time()}
        return check_nulls
