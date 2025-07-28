from django.urls import path
from .views import ProductAPIViews

urlpatterns = [
    path('products/', ProductAPIViews.as_view()),                     # List all products
    path('create-products/', ProductAPIViews.as_view()),              # Create new product
    path('get-product/<int:id>/', ProductAPIViews.as_view()),         # Retrieve product
    path('update-products/<int:id>/', ProductAPIViews.as_view()),     # Update product
    path('delete-products/<int:id>/', ProductAPIViews.as_view()),     # Delete product
]
