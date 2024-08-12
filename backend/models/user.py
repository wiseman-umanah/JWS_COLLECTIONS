#!/usr/bin/python3
from backend.models.base import BaseModel
import bcrypt
import re

class User(BaseModel):
    def __init__(self, *args, **kwargs):
        """
        Initialize a new User instance.
        """
        super().__init__(*args, **kwargs)
        
        # Default attribute values
        self.username = ""
        self.firstname = ""
        self.lastname = ""
        self._password = ""  # Use a private attribute for the password
        self._email = ""
        self.phoneNumber = ""
        self.items_id = []  # track user items id (user relationship with shoe)
        self.is_authenticated = True

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__" and hasattr(self, key):
                    setattr(self, key, value)
    
    def set_password(self, password):
        """
        Set the user's password with validation and hashing.
        """
        self._password = self.hash_password(password)
    
    @staticmethod
    def hash_password(password):
        """
        Hash the password using bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    def check_password(self, password):
        """
        Check the password against the stored hashed password.
        
        """
        return bcrypt.checkpw(password.encode('utf-8'), self._password)
    
    def validate_email(self, email):
        """
        Validate the email format.
        """
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_regex, email) is not None
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if self.validate_email(value):
            self._email = value
        else:
            raise ValueError("Invalid email format")
