from rest_framework import serializers

from .models import Customer, Item, Order, User


class ItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CustomerSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)


class OrderSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    customer = CustomerSerializer()
    item = ItemSerializer()
    quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Hash the password before saving
        from django.contrib.auth.hashers import make_password
        password = validated_data.pop("password")
        validated_data["password"] = make_password(password)
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Hash password if it's being updated
        if "password" in validated_data:
            from django.contrib.auth.hashers import make_password
            validated_data["password"] = make_password(validated_data["password"])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
