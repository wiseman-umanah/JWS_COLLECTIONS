from backend.models.base import BaseModel

class Order(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
        """order status"""
        return self._status

    @status.setter
    def status(self, value: str):
        """Update order status"""
        self._status = value
            
    def calculate_total(self):
        """Calculate the total price of the order."""
        self.total_price = sum(item.total_price for item in self.items)

    def to_dict(self):
        """Convert Cart to a dictionary for JSON serialization"""
        dict_cart = super().to_dict()
        dict_cart.update({
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total_price': self.total_price,
            'status': self.status
        })
        return dict_cart
    