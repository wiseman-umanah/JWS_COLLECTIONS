#!/usr/bin/python3
from backend.models.engine.file_storage import FileStorage


storage = FileStorage()

storage.reload()

# Import models here to avoid circular imports
from backend.models.user import User
from backend.models.shoe import Shoe

# Make the storage and models available at the package level
__all__ = ["storage", "User", "Shoe"]

