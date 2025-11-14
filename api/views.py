from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.services.auth import login, register
from api.services.customers import getCustomer, getCustomers
from api.services.orders import createOrder, getOrder, getOrders

from .services.items import (createItem, deleteItem, getItem, getItems,
                             updateItem)


@api_view(["GET", "POST"])
def items_management(request):
    """
    Handle GET (list all items) and POST (create new item) requests.
    """
    if request.method == "GET":
        items = getItems()
        return Response(items, status=status.HTTP_200_OK)

    elif request.method == "POST":
        result = createItem(request.data)
        if result["success"]:
            return Response(result["data"], status=status.HTTP_201_CREATED)
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["GET", "PUT", "DELETE", "PATCH"])
def item_management(request, pk):
    """
    Handle GET (retrieve), PUT (full update), PATCH (partial update),
    and DELETE requests for a specific item.
    """
    if request.method == "GET":
        item = getItem(pk)
        if item:
            return Response(item, status=status.HTTP_200_OK)
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "DELETE":
        deleted = deleteItem(pk)
        if deleted:
            return Response(
                {"message": "Item deleted successfully"}, status=status.HTTP_200_OK
            )
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PATCH":
        # Partial update - only update provided fields
        result = updateItem(pk, request.data, partial=True)
        if result["success"]:
            return Response(result["data"], status=status.HTTP_200_OK)
        if result.get("not_found"):
            return Response(result["errors"], status=status.HTTP_404_NOT_FOUND)
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        # Full update - replace all fields
        result = updateItem(pk, request.data, partial=False)
        if result["success"]:
            return Response(result["data"], status=status.HTTP_200_OK)
        if result.get("not_found"):
            return Response(result["errors"], status=status.HTTP_404_NOT_FOUND)
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["GET", "POST"])
def orders_management(request):
    """
    Handle GET (list all orders) and POST (create new order) requests.
    """
    if request.method == "GET":
        orders = getOrders()
        return Response(orders, status=status.HTTP_200_OK)

    elif request.method == "POST":
        result = createOrder(request.data)
        if result["success"]:
            return Response(result["data"], status=status.HTTP_201_CREATED)
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["GET", "PUT", "DELETE", "PATCH"])
def order_management(request, pk):
    """
    Handle GET (retrieve), PUT (full update), PATCH (partial update),
    and DELETE requests for a specific order.
    """
    if request.method == "GET":
        order = getOrder(pk)
        if order["success"]:
            return Response(order["data"], status=status.HTTP_200_OK)
        return Response(order["errors"], status=status.HTTP_404_NOT_FOUND)

    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["GET"])
def customers_management(request):
    """
    Handle GET (list all customers) requests.
    """
    if request.method == "GET":
        customers = getCustomers()
        return Response(customers, status=status.HTTP_200_OK)
    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["GET"])
def customer_management(request, pk):
    """
    Handle GET (retrieve) requests for a specific customer.
    """
    if request.method == "GET":
        customer = getCustomer(pk)
        if customer["success"]:
            return Response(customer["data"], status=status.HTTP_200_OK)
        return Response(customer["errors"], status=status.HTTP_404_NOT_FOUND)
    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """
    Handle POST (register new user) requests.
    Public endpoint - no authentication required.
    """
    if request.method == "POST":
        result = register(request.data)
        if result["success"]:
            return Response(result["data"], status=status.HTTP_201_CREATED)
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Handle POST (login user) requests.
    Public endpoint - no authentication required.
    """
    if request.method == "POST":
        result = login(request.data)
        if result["success"]:
            return Response(result["data"], status=status.HTTP_200_OK)
        return Response(result["errors"], status=status.HTTP_401_UNAUTHORIZED)
    return Response(
        {"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
