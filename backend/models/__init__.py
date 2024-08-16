#!/usr/bin/python3
from backend.models.engine.file_storage import FileStorage


storage = FileStorage()

storage.reload()

# Import models here to avoid circular imports
from backend.models.user import User
from backend.models.shoe import Shoe
from backend.models.cart import Cart
from backend.models.cartitem import CartItem

# Make the storage and models available at the package level
__all__ = ["db", "storage", "User", "Shoe", "Cart", "CartItem"]

