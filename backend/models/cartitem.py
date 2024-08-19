#!/usr/bin/python3
"""CartItem model for each item in cart"""
from backend.models.base import BaseModel, Base
from sqlalchemy import Column, String, Float, ForeignKey
from backend.models import method


class CartItem(BaseModel, Base):
    """CartItem model

    Args:
        BaseModel (Class): the base model
        Base (declarative base): the table model
    """
    if method == 'db':
        __tablename__ = 'cart_items'
        cart_id = Column(String(100), ForeignKey('carts.id'), nullable=False)
        shoe_id = Column(String(100), nullable=False)
        shoe_name = Column(String(128), nullable=False)
        quantity = Column(Float, nullable=False)
        _price = Column(Float, nullable=False)
        _total_price = Column(Float, nullable=False)
        order_id = Column(String(100), ForeignKey('orders.id'), nullable=True) 


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if method != 'db':
            self.cart_id = ""
            self.shoe_id = ""
            self.shoe_name = ""
            self.quantity = 0
            self._price = 0.0
            self._total_price = 0.0
            self.order_id = ""

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    @property
    def price(self) -> float:
        """Get price of cart item

        Returns:
            float: float repr of product (shoe) price
        """
        return self._price

    @price.setter
    def price(self, value: float):
        """Set new price of cart item

        Args:
            value (float): the new price

        Raises:
            ValueError: cart item cannot be non-negative
        """
        if isinstance(value, (int, float)) and value >= 0:
            self._price = float(value)
        else:
            raise ValueError("Cart item price must be a non-negative number")

    @property
    def total_price(self) -> float:
        """Retrieve total price

        Returns:
            float: the total price of cart item
        """
        return self._total_price

    @total_price.setter
    def total_price(self, value: float):
        """Sets a new total price

        Args:
            value (float): the new price to update to

        Raises:
            ValueError: price cannot be < 0
        """
        if isinstance(value, (int, float)) and value >= 0:
            self._total_price = float(value)
        else:
            raise ValueError("Cart item price must be a non-negative number")
        
    def update_total_price(self):
        """Updates total price based on quantity"""
        self.total_price = self.quantity * self.price

    def to_dict(self):
        """Returns the dictionary representation of cart item"""
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'shoe_id': self.shoe_id,
            'shoe_name': self.shoe_name,
            'quantity': self.quantity,
            'price': self.price,
            'total_price': self.total_price,
            'order_id': self.order_id,
        }
