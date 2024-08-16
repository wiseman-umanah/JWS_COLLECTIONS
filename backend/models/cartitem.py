#!/usr/bin/python3
from backend.models.base import BaseModel


class CartItem(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cart_id = ""
        self.shoe_id = ""
        self.shoe_name = ""
        self.quantity = 0
        self._price = 0.0
        self._total_price = 0.0

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

        @property
        def price(self) -> float:
            """cart item price"""
            return self._price
    
        @price.setter
        def price(self, value: float):
            """Update price of a cart item"""
            if isinstance(value, (int, float)) and value >= 0:
                self._price = float(value)
            else:
                raise ValueError("Cart item price must be a non-negative number")

        @property
        def total_price(self) -> float:
            """cart item price"""
            return self._total_price
    
        @total_price.setter
        def _total_price(self, value: float):
            """Update price of a cart item"""
            if isinstance(value, (int, float)) and value >= 0:
                self._total_price = float(value)
            else:
                raise ValueError("Cart item price must be a non-negative number")
            
        def update_total_price(self):
            self.total_price = self.quantity * self.price
