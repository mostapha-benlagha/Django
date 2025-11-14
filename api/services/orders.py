from api.models import Order
from api.models import Item
from api.models import Customer
from mongoengine.errors import DoesNotExist
from mongoengine.errors import ValidationError
from bson.errors import InvalidId
from api.serializers import OrderSerializer


def getOrders():
    orders = list(Order.objects.all())
    # Populate customer and item references
    for order in orders:
        _ = order.customer  # Trigger dereference
        _ = order.item  # Trigger dereference
    serializer = OrderSerializer(orders, many=True)
    return serializer.data


def createOrder(data):
    # Validate customer data
    customerData = data.get("customer")
    if not customerData:
        return {"success": False, "errors": {"customer": "Customer data is required"}}

    email = customerData.get("email")
    customer_name = customerData.get("name")

    if not email:
        return {"success": False, "errors": {"email": "Customer email is required"}}
    if not customer_name:
        return {"success": False, "errors": {"name": "Customer name is required"}}

    # Get or create customer
    try:
        customer = Customer.objects.get(email=email)
    except DoesNotExist:
        try:
            customer = Customer.objects.create(name=customer_name, email=email)
        except ValidationError as e:
            return {"success": False, "errors": {"customer": str(e)}}

    # Validate and get item
    itemId = data.get("itemId")
    if not itemId:
        return {"success": False, "errors": {"itemId": "Item ID is required"}}

    try:
        item = Item.objects.get(id=itemId)
    except (DoesNotExist, ValidationError, InvalidId) as e:
        if isinstance(e, InvalidId) or isinstance(e, ValidationError):
            return {"success": False, "errors": {"itemId": "Invalid item ID format"}}
        return {"success": False, "errors": {"item": "Item not found"}}

    # Validate quantity
    quantity = data.get("quantity")
    if quantity is None:
        return {"success": False, "errors": {"quantity": "Quantity is required"}}

    # Create order
    try:
        order = Order.objects.create(
            customer=customer, item=item, quantity=quantity
        )
        # Populate references for serialization
        _ = order.customer
        _ = order.item
        return {"success": True, "data": OrderSerializer(order).data}
    except ValidationError as e:
        return {"success": False, "errors": {"order": str(e)}}


def getOrder(id):
    try:
        order = Order.objects.get(id=id)
        # Populate customer and item references
        _ = order.customer  # Trigger dereference
        _ = order.item  # Trigger dereference
        return {"success": True, "data": OrderSerializer(order).data}
    except DoesNotExist:
        return {"success": False, "errors": {"detail": "Order not found"}}
