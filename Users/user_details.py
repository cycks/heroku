"""This file contains a single class that is used to extract
user details from the post request."""
import jwt
# import re
from flask import request


class UserDetails:
    """A class used to extract user details from the post request"""
    def __init__(self, details_from_post=None):
        if details_from_post is None:
            self.details_from_post = request.get_json()
        else:
            self.details_from_post = details_from_post

    @staticmethod
    def check_detail_length(detail):
        """Method used to validate user detail"""
        if len(detail) > 60 or len(detail) < 5 or "execute" in detail:
            return False
        return True

    def get_first_name(self):
        """"Used to extract user's first name."""
        first_name = self.details_from_post.get("first_name", None)
        if self.check_detail_length(first_name)is True:
            return first_name
        return False

    def get_last_name(self):
        """Used to extract user's last name"""
        last_name = self.details_from_post.get("last_name", None)
        if self.check_detail_length(last_name) is True:
            return last_name
        return False

    def get_email(self):
        """"Used to extract user's email"""
        email = self.details_from_post.get("email", None)
        if self.check_detail_length(email) is True:
            return email
        return False

    def get_password(self):
        """Used to extract user's password"""
        password = self.details_from_post.get("password1", None)
        if self.check_detail_length(password) is True:
            return password
        return False

    def get_password2(self):
        """Used to extract user's password2."""
        password2 = self.details_from_post.get("password2", None)
        if self.check_detail_length(password2) is True:
            return password2
        return False

    def get_user_name(self):
        """Used to extract user's username"""
        user_name = self.details_from_post.get("user_name", None)
        if self.check_detail_length(user_name) is True:
            return user_name
        return False

    def get_user_id(self):
        """Used to extract user's id from the token supplied
        by a request."""
        try:
            user_id = jwt.decode(request.args.get("user_token"),
                                 "This is not the owner")['user']
            return user_id
        except jwt.exceptions.DecodeError:
            return False
        except jwt.exceptions.ExpiredSignatureError:
            return False

    @property
    def combine_details(self):
        """combines all the registration details into a dictionary and checks
        if any of the details is none. It returns the name of the detail that
        is not validated by the check length  method in this class."""
        check_nulls = {"first_name": self.get_first_name(),
                       "last_name": self.get_last_name(),
                       "email": self.get_email(),
                       "user_name": self.get_user_name(),
                       "password": self.get_password()}
        return check_nulls

    @property
    def validate_details(self):
        """Uses the combine_details method to """
        for detail in self.combine_details:
            if self.combine_details[detail] is False:
                return detail
        return None
# class ValidateLogin(UserDetails):
#     """Inherits from the user details class and validates login credentials"""
#     def combine_details(self):
#         """combines all the login details into a dictionary and checks if
#         any of the details is none. It returns the name of the detail that
#         is not validated by the check length  method in this class."""
#         check_nulls = {"email": self.get_email(),
#                        "password": self.get_password()}
#         for detail in check_nulls:
#             if check_nulls[detail] is False:
#                 return detail
#         return None
