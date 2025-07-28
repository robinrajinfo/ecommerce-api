from django.urls import path
from .views import (
    CustomerRegistrationAPIView,
    CustomerLoginAPIView,
    CustomerProfileAPIView,
    CustomerListView,  # Make sure this view exists
)

urlpatterns = [
    # 🔹 Endpoint to register a new customer
    path("register/", CustomerRegistrationAPIView.as_view(), name="customer-register"),

    # 🔹 Endpoint for customer login
    path("login/", CustomerLoginAPIView.as_view(), name="customer-login"),

    # 🔹 Endpoint to get customer profile by ID
    path("profile/<int:customer_id>/", CustomerProfileAPIView.as_view(), name="customer-profile"),

    # 🔹 Optional: view all customers (for admin/debugging)
    path("all/", CustomerListView.as_view(), name="customer-list"),
]
