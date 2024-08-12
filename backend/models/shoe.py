#!/usr/bin/python3
"""Shoe Model Class
"""
from base import BaseModel


class Shoe(BaseModel):
    """Shoe model

    Args:
        BaseModel (class): base model for classes
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.shoe_name = ""
            self.shoe_category = ""
            self.shoe_brand = ""
            self.shoe_price = ""
            self.shoe_color = ""
        