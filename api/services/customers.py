from bson.errors import InvalidId
from mongoengine import DoesNotExist, ValidationError

from ..models import Customer
from ..serializers import CustomerSerializer


def getCustomers():
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return serializer.data


def getCustomer(id):
    try:
        customer = Customer.objects.get(id=id)
        serializer = CustomerSerializer(customer)
        return {"success": True, "data": serializer.data}
    except (DoesNotExist, ValidationError, InvalidId):
        return {"success": False, "errors": {"detail": "Customer not found"}}
