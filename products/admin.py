from django.contrib import admin
from .models import ProductCategory, ProductSubcategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'organisation', 'is_active', 'created_at')
    search_fields = ('category_name',)
    list_filter = ('organisation', 'is_active')
    ordering = ('-created_at',)


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategory_name', 'organisation', 'category', 'is_active', 'created_at')
    search_fields = ('subcategory_name',)
    list_filter = ('organisation', 'category', 'is_active')
    ordering = ('-created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product_name', 'organisation', 'category', 'subcategory',
        'price', 'discount_price', 'stock_quantity', 'availability', 'product_type', 'created_at'
    )
    search_fields = ('product_name', 'category_name', 'subcategory_name')
    list_filter = ('organisation', 'category', 'subcategory', 'availability', 'product_type')
    ordering = ('-created_at',)
