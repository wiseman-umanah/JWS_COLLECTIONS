#!/usr/bin/python3
"""Order model for handling orders"""
from backend.models.base import BaseModel, Base
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.models import method
from backend.models.cartitem import CartItem


class Order(BaseModel, Base):
    """Order model

    Args:
        BaseModel (class): the base model of class
        Base (declarative base): the table model
    """
    if method == 'db':
        __tablename__ = 'orders'
        user_id = Column(String(100), ForeignKey('users.id'), nullable=False)
        total_price = Column(Float, nullable=False, default=0.0)
        _status = Column(String(50), nullable=False, default="pending")
        items = relationship('CartItem', backref='order', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if method != 'db':
            self.user_id = ""
            self.items = []  # List of CartItems
            self.total_price = 0.0
            self._status = "pending"

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    @property
    def status(self) -> str:
        """order status

        Returns:
            str: current status
        """
        return self._status

    @status.setter
    def status(self, value: str):
        """Update order status

        Args:
            value (str): the status to change
        """
        self._status = value

    def calculate_total(self):
        """Calculate the total price of the order."""
        self.total_price = sum(item.total_price for item in self.items)

    def to_dict(self):
        """Convert Order to a dictionary for JSON serialization"""
        dict_order = super().to_dict()
        dict_order.update({
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items if isinstance(item, CartItem)],
            'total_price': self.total_price,
            'status': self.status
        })
        return dict_order
