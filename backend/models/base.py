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
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if 'created_at' in kwargs:
                self.created_at = datetime.strptime(kwargs['created_at'], time)
            if 'updated_at' in kwargs:
                self.updated_at = datetime.strptime(kwargs['updated_at'], time)

    def __str__(self) -> str:
        """string representation of class models

        Returns:
            str: string representation of class
        """
        classname = self.__class__.__name__
        return '[{}] ({}) {}'.format(classname, self.id, self.__dict__)

    def save(self):
        from backend.models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()
    
    def to_dict(self) -> dict:
        """Converts object to dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        try:
            if not isinstance(dictionary['created_at'], str):
                dictionary['created_at'] = self.created_at.strftime(time)
            if not isinstance(dictionary['updated_at'], str):
                dictionary['updated_at'] = self.updated_at.strftime(time)
        except AttributeError as e:
            print(f"Error converting to dictionary: {e}")
        return dictionary

    
    def delete(self):
        """Delete an instance from the storage"""
        from backend.models import storage
        storage.delete(self)
        storage.save()
        
