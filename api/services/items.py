from bson.errors import InvalidId
from mongoengine import ValidationError
from ..models import Item
from ..serializers import ItemSerializer
from mongoengine.errors import DoesNotExist


def getItems():
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return serializer.data


def getItem(id):
    try:
        item = Item.objects.get(id=id)
        serializer = ItemSerializer(item)
        return serializer.data
    except (DoesNotExist, ValidationError, InvalidId):
        return False


def createItem(data):
    serializer = ItemSerializer(data=data)
    if serializer.is_valid():
        item = serializer.save()
        # Return the serialized data after save
        return {"success": True, "data": ItemSerializer(item).data}
    return {"success": False, "errors": serializer.errors}


def updateItem(pk, data, partial=True):
    try:
        item = Item.objects.get(id=pk)
        serializer = ItemSerializer(item, data=data, partial=partial)
        if serializer.is_valid():
            updated_item = serializer.save()
            return {"success": True, "data": ItemSerializer(updated_item).data}
        return {"success": False, "errors": serializer.errors, "not_found": False}
    except DoesNotExist:
        return {
            "success": False,
            "errors": {"detail": "Item not found"},
            "not_found": True,
        }


def deleteItem(id):
    try:
        item = Item.objects.get(id=id)
        item.delete()
        return True
    except DoesNotExist:
        return False
