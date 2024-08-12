from backend.models.base import BaseModel

class User(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.username = ""
            self.firstname = ""
            self.lastname = ""
            self.password = ""
            self.email = "example@gmail.com"
            self.phoneNumber = 12345678
            self.items_id = [] # track user items id (user relationship with shoe)
