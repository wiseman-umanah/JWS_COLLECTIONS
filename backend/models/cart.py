from backend.models.base import BaseModel
from backend.models import storage
from backend.models.cartitem import CartItem

class Cart(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_id = ""
        self.items = []

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    def add_item(self, shoe_id, quantity, price):
        """Add an item to the cart or update quantity if it already exists"""
        for item in self.items:
            if item.shoe_id == shoe_id:
                item.quantity += quantity
                item.update_total_price()
                return

        new_item = CartItem(cart_id=self.id, shoe_id=shoe_id, quantity=quantity, price=price)
        self.items.append(new_item)

    def update_quantity(self, shoe_id, quantity):
        """Update the quantity of an item in the cart"""
        for item in self.items:
            if item.shoe_id == shoe_id:
                item.quantity = quantity
                item.update_total_price()
                return

    def remove_item(self, shoe_id):
        """Remove an item from the cart"""
        self.items = [item for item in self.items if item.shoe_id != shoe_id]

    def calculate_total(self):
        """Calculate the total price of the cart"""
        return sum(item.total_price for item in self.items)
