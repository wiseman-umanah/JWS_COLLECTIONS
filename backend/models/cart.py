#!/usr/bin/python3
"""Cart Model to handle cart of users"""
from backend.models.base import BaseModel, Base
from backend.models.cartitem import CartItem
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.models import method


class Cart(BaseModel, Base):
    """Cart Model of users

    Args:
        BaseModel (Class): The Basemodel
        Base (declarative_base): the table model
    """
    if method == 'db':
        __tablename__ = 'carts'
        user_id = Column(String(100), ForeignKey('users.id'), nullable=False)
        items = relationship('CartItem', backref='cart', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if method != 'db':
            self.user_id = ""
            self.items = []

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    def add_item(self, shoe_name: str, shoe_id: str, quantity: int, price: float):
        """Add an item to the cart or update quantity if it already exists

        Args:
            shoe_name (str): the shoe name to add to cart
            shoe_id (str): the shoe id to add
            quantity (int): quantity to add
            price (float): the price of the product(shoe)
        """
        item = next((i for i in self.items if i.shoe_id == shoe_id), None)
        if item:
            item.quantity += quantity
            item.total_price = item.quantity * price
        else:
            new_item = CartItem(
                cart_id=self.id, shoe_name=shoe_name,
                shoe_id=shoe_id, quantity=quantity,
                price=price, total_price=quantity * price)
            self.items.append(new_item)

    def update_quantity(self, shoe_id: str, quantity: int):
        """Update the quantity of an item in the cart

        Args:
            shoe_id (str): the shoe id to update
            quantity (int): the quantity to add
        """
        item = next((i for i in self.items if i.shoe_id == shoe_id), None)
        if item:
            item.quantity = quantity
            item.update_total_price()

    def remove_item(self, shoe_id: str):
        """Remove an item from the cart

        Args:
            shoe_id (str): the id of the product (shoe)
        """
        self.items = [item for item in self.items if item.shoe_id != shoe_id]

    def calculate_total(self):
        """Calculate the total price of the cart"""
        return sum(item.total_price for item in self.items)

    def to_dict(self):
        """Convert Cart to a dictionary for JSON serialization"""
        dict_cart = super().to_dict()
        dict_cart.update({
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items]
        })
        return dict_cart

    def to_order(self):
        """Convert the cart into an order"""
        from backend.models.order import Order

        order = Order(user_id=self.user_id)
        order.items = self.items[:]
        order.calculate_total()
        return order
