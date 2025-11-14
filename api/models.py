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
