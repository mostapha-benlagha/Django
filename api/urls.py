from .views import items_management, item_management, register_view, login_view
from .views import orders_management, order_management
from .views import customers_management, customer_management
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("orders/", orders_management, name="orders_management"),
    path("orders/<str:pk>", order_management, name="order_management"),
    path("customers/", customers_management, name="customers_management"),
    path("customers/<str:pk>", customer_management, name="customer_management"),
    path("auth/login/", login_view, name="token_obtain_pair"),
    path("auth/register/", register_view, name="register"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", items_management, name="items_management"),
    path("<str:pk>", item_management, name="item_management"),
]
