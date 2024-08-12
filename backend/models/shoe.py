#!/usr/bin/python3
"""Shoe Model Class
"""
from backend.models.base import BaseModel


class Shoe(BaseModel):
    """Shoe model
    
    Args:
        BaseModel (class): base model for classes
    """
    def __init__(self, *args, **kwargs):
        """Initialize a new Shoe instance."""
        super().__init__(*args, **kwargs)
        
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
        """shoe price

        Returns:
            float: returns shoe price
        """
        return self._shoe_price

    @shoe_price.setter
    def shoe_price(self, value: float):
        """Update price of a shoe"""
        if isinstance(value, (int, float)) and value >= 0:
            self._shoe_price = float(value)
        else:
            raise ValueError("Shoe price must be a non-negative number")

    @property
    def shoe_image(self) -> str:
        """get shoe image path

        Returns:
            str: path to image
        """
        return self._shoe_image

    @shoe_image.setter
    def shoe_image(self, value: str):
        """Set path to image"""
        if isinstance(value, str) and value.startswith(("http://", "https://", "/")):
            self._shoe_image = value
        else:
            raise ValueError("Shoe image must be a valid URL or path")
