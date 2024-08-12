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
        super().__init__(*args, **kwargs)
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.shoe_name = "" # name of shoe like sneakers etc
            self.shoe_category = "" # category like for men, women or sports
            self.shoe_brand = "" # brand like nike etc
            self.shoe_price = "" # price of shoe
            self.shoe_color = "" # the color of shoe
        