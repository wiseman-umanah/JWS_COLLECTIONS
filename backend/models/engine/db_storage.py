#!/usr/bin/python3
"""Database Storage Engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.models.base import Base
from backend.models.shoe import Shoe
from backend.models.user import User
from backend.models.cart import Cart
from backend.models.cartitem import CartItem
from backend.models.order import Order
from os import getenv
from dotenv import load_dotenv


load_dotenv()

classes = {"User": User, "Shoe": Shoe,
           "Cart": Cart, "CartItem": CartItem,
           "Order": Order}


class DBStorage:
    """Interacts with the database"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage"""
        DB_USER = getenv('DB_USER')
        DB_PASSWORD = getenv('DB_PASSWORD')
        DB_HOST = getenv('DB_HOST')
        DB_PORT = getenv('DB_PORT', '12880')
        DB_NAME = getenv('DB_NAME')
        SSL_CA = getenv('SSL_CA', 'ca.pem')  # Path to your ca.pem file

        self.__engine = create_engine(
            f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
            connect_args={
                "ssl": {
                    "ssl_ca": SSL_CA
                }
            }
        )
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

        Base.metadata.create_all(self.__engine)

    def all(self, cls=None):
        """Retrieves all data from db or based on cls

        Args:
            cls (object, optional): the class model. Defaults to None.

        Returns:
            dict: the objects that have been retrieved
        """
        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in self.__session.query(cls).all()}
        else:
            all_objects = {}
            for class_name in classes.values():
                all_objects.update({f"{obj.__class__.__name__}.{obj.id}": obj for obj in self.__session.query(class_name).all()})
            return all_objects

    def new(self, obj):
        """Adds an object to db

        Args:
            obj (object): the object to add
        """
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def reload(self):
        """Create all tables in the database and initialize a new session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    def delete(self, obj=None):
        """Deletes a data from database

        Args:
            obj (object, optional): the object to delete. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)
            self.save()

    def close(self):
        """Remove the session"""
        self.__session.remove()

    def get_user_by_email(self, email):
        """Retrieves user based on email

        Args:
            email (str): the email of the user

        Returns:
            object: the user object
        """
        return self.__session.query(User).filter_by(_email=email).first()

    def get_cart_by_userId(self, user_id):
        """Get cart by user ID

        Args:
            user_id (str): the id of the user

        Returns:
            object: the cart associated with the user
        """
        cart = self.__session.query(Cart).filter_by(user_id=user_id).first()
        if cart:
            cart.items = [CartItem(**item.to_dict()) if isinstance(item, dict) else item for item in cart.items]
        return cart

    def get(self, cls, id):
        """Returns the object based on class name and ID

        Args:
            cls (object): The object class
            id (str): id of the object

        Returns:
            object: the object to retrieve | None
        """
        if cls in classes.values():
            return self.__session.query(cls).filter_by(id=id).first()
        return None

    def count(self, cls=None):
        """Count the number of objects in storage

        Args:
            cls (object, optional): the class of the model. Defaults to None.

        Returns:
            int: the count of the objects
        """
        if cls:
            return self.__session.query(cls).count()
        else:
            return sum(self.__session.query(class_name).count() for class_name in classes.values())
