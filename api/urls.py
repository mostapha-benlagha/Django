from .views import items_management, item_management
from .views import orders_management, order_management
from .views import customers_management, customer_management
from django.urls import path


urlpatterns = [
    path("", items_management, name="items_management"),
    path("<str:pk>", item_management, name="item_management"),
    path("orders/", orders_management, name="orders_management"),
    path("orders/<str:pk>", order_management, name="order_management"),
    path("customers/", customers_management, name="customers_management"),
    path("customers/<str:pk>", customer_management, name="customer_management"),
]
