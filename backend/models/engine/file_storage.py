#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from backend.models.shoe import Shoe
from backend.models.user import User


classes = {"User": User, "Shoe": Shoe}

class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "database.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            new_dict = {key: value for key, value in self.__objects.items() if isinstance(value, cls)}
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Save objects to a JSON file"""
        json_objects = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except FileNotFoundError:
            print("File not found. Starting with an empty storage.")
        except json.JSONDecodeError:
            print("Error decoding JSON. The file may be corrupted.")
        except KeyError as e:
            print(f"Missing class {e} in JSON data.")


    def delete(self, obj=None):
        """delete obj from __object if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get_user_by_email(self, email):
        """Returns the user object based on email"""
        all_cls = self.all(User)
        for value in all_cls.values():
            if value.email == email:
                return value
        return None

    def get(self, cls, id):
        """Returns the object based on class name and ID"""
        if cls not in classes.values():
            return None
        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value
        return None


    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls:
            return len(self.all(cls).values())
        return len(self.__objects)

