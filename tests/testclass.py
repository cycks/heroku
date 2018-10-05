from Users.user_details import UserDetails

import unittest
import json


class TestUserClass(unittest.TestCase):
    """This class tests the functionality of the class UserDetails from the
    user_details file."""

    def setUp(self):
        self.test1 = UserDetails({'first_name': 'firstname',
                                  'last_name': 'lastname',
                                  'email': 'sikolia2.wycliffe@gmail.com',
                                  'user_name': 'cycks1', 'password': 'password',
                                  'password2': 'password'})


    def tearDown(self):
        pass

    def test_appropriate_details(self):
        """Tests that an approrpiate log in will be successful"""

