#!/usr/bin/python3
"""Shoe Model Class
"""
from backend.models.base import BaseModel, Base
from sqlalchemy import Column, String, Float
from backend.models import method


class Shoe(BaseModel, Base):
    """Shoe model

    Args:
        BaseModel (class): base model for classes
        Base (declarative base): the table model
    """
    if method == 'db':
        __tablename__ = 'shoes'
        shoe_name = Column(String(128), nullable=False)
        shoe_category = Column(String(128), nullable=False)
        shoe_brand = Column(String(128), nullable=False)
        _shoe_price = Column(Float, nullable=False, default=0.0)
        shoe_color = Column(String(128), nullable=False)
        _shoe_image = Column(String(256), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new Shoe instance."""
        super().__init__(*args, **kwargs)

        if method != 'db':
            self.shoe_name = ""
            self.shoe_category = ""
            self.shoe_brand = ""
            self._shoe_price = 0.0
            self.shoe_color = ""
            self._shoe_image = ""

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    @property
    def shoe_price(self) -> float:
        """Shoe price"""
        return self._shoe_price

    @shoe_price.setter
    def shoe_price(self, value: float):
        """Update price of a shoe

        Args:
            value (float): the new shoe price

        Raises:
            ValueError: price must not be < 0
        """
        if isinstance(value, (int, float)) and value >= 0:
            self._shoe_price = float(value)
        else:
            raise ValueError("Shoe price must be a non-negative number")

    @property
    def shoe_image(self) -> str:
        """Get shoe image path"""
        return self._shoe_image

    @shoe_image.setter
    def shoe_image(self, value: str):
        """Sets image path

        Args:
            value (str): the image path

        Raises:
            ValueError: shoe must be a valid path
        """
        if isinstance(value, str) and value.startswith(("http://", "https://", "/")):
            self._shoe_image = value
        else:
            raise ValueError("Shoe image must be a valid URL or path")
