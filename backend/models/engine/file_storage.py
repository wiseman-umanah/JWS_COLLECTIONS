#!/usr/bin/python3
"""
Contains the FileStorage class
"""
import json
from backend.models.shoe import Shoe
from backend.models.user import User
from backend.models.cart import Cart
from backend.models.cartitem import CartItem
from backend.models.order import Order


classes = {"User": User, "Shoe": Shoe,
           "Cart": Cart, "CartItem": CartItem,
           "Order": Order}

class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "database.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """Retrieves all data from file or based on cls

        Args:
            cls (object, optional): the class model. Defaults to None.

        Returns:
            dict: the objects that have been retrieved
        """
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            new_dict = {key: value for key, value in self.__objects.items() if isinstance(value, cls)}
            return new_dict
        return self.__objects

    def new(self, obj):
        """Adds an object to file

        Args:
            obj (object): the object to add
        """
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
            for key, value in jo.items():
                cls = classes.get(value["__class__"])
            if cls:
                self.__objects[key] = cls(**value)
            else:
                print(f"Class {value['__class__']} not found.")
        except FileNotFoundError:
            print("File not found. Starting with an empty storage.")
        except json.JSONDecodeError:
            print("Error decoding JSON. The file may be corrupted.")
        except KeyError as e:
            print(f"Missing class {e} in JSON data.")


    def delete(self, obj=None):
        """Deletes a data from file

        Args:
            obj (object, optional): the object to delete. Defaults to None.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get_user_by_email(self, email):
        """Retrieves user based on email

        Args:
            email (str): the email of the user

        Returns:
            object: the user object
        """
        all_cls = self.all(User)
        for value in all_cls.values():
            if value.email == email:
                return value
        return None
    
    def get_cart_by_userId(self, user_id):
        """Get cart by user ID

        Args:
            user_id (str): the id of the user

        Returns:
            object: the cart associated with the user
        """
        for cart in self.all(Cart).values():
            if cart.user_id == user_id:
                # Ensure items are CartItem instances
                cart.items = [CartItem(**item) if isinstance(item, dict) else item for item in cart.items]
                return cart
        return None

    def get(self, cls, id):
        """Returns the object based on class name and ID

        Args:
            cls (object): The object class
            id (str): id of the object

        Returns:
            object: the object to retrieve | None
        """
        if cls not in classes.values():
            return None
        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value
        return None


    def count(self, cls=None):
        """Count the number of objects in storage

        Args:
            cls (object, optional): the class of the model. Defaults to None.

        Returns:
            int: the count of the objects
        """
        if cls:
            return len(self.all(cls).values())
        return len(self.__objects)

