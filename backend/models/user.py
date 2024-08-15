from backend.models.base import BaseModel
from hashlib import md5
import re
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = ""
        self.firstname = ""
        self.lastname = ""
        self._password = ""
        self._email = ""
        self.phoneNumber = ""
        self.role = "user"

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__" and hasattr(self, key):
                    setattr(self, key, value)

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)
    
    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value: str):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, value):
            self._email = value
        else:
            raise ValueError('Invalid Email')

    def from_dict(self):
        dictionary = self.to_dict()
        del dictionary['_password']
        return dictionary