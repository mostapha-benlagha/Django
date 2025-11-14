from mongoengine import Document, IntField, StringField, DateTimeField, ReferenceField
from datetime import datetime


class Item(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(required=False)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "items"}

    def __str__(self):
        return self.name


class Customer(Document):
    name = StringField(max_length=100, required=True)
    email = StringField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "customers"}

    def __str__(self):
        return self.name


class Order(Document):
    quantity = IntField(required=True)
    customer = ReferenceField(Customer, required=True)
    item = ReferenceField(Item, required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "orders"}

    def __str__(self):
        return f"{self.quantity} {self.item.name}"


class User(Document):
    username = StringField(max_length=100, required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "users"}

    def __str__(self):
        return self.username

    @property
    def is_authenticated(self):
        """Required by Django REST Framework for authentication checks."""
        return True

    @property
    def is_active(self):
        """Required by Django REST Framework for permission checks."""
        return True

    @property
    def is_anonymous(self):
        """Required by Django REST Framework for authentication checks."""
        return False