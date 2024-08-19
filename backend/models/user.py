from backend.models.base import BaseModel, Base
import re
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import method
from sqlalchemy import Column, String

class User(BaseModel, Base):
    if method == 'db':
        __tablename__ = 'users'
        username = Column(String(128), nullable=False)
        firstname = Column(String(128), nullable=False)
        lastname = Column(String(128), nullable=False)
        _password = Column('password', String(1024), nullable=False)
        _email = Column('email', String(128), nullable=False)
        role = Column(String(128), nullable=False, default='user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if method != 'db':
            self.username = ""
            self.firstname = ""
            self.lastname = ""
            self._password = ""
            self._email = ""
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
