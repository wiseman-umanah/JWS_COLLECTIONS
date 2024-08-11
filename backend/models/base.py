#!/usr/bin/python3
"""
Base Model to handle all models
"""
import uuid
from datetime import datetime


time = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    def __init__(self, *args, **kwargs):
        """Initializes a base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and isinstance(self.created_at, str):
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            if kwargs.get("updated_at", None) and isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
    
    def __str__(self) -> str:
        """string representation of class models

        Returns:
            str: string representation of class
        """
        classname = self.__class__.__name__
        return '[{}] ({}) {}'.format(classname, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.utcnow()
        pass
    
    def to_dict(self) -> dict:
        """Converts object to dict format

        Returns:
            dict: dictionary rep of the object
        """
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.strftime(time)
        dictionary['updated_at'] = self.updated_at.strftime(time)
        return dictionary
    
    def delete(self):
        """Delete an instance from the storage"""
        pass
