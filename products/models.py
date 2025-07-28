from datetime import date

from django.db import models

from organisations.models import (
    Organisation
)


class ProductCategory(models.Model):
    class Meta:
        verbose_name_plural = 'product_categories'

    id: models.AutoField = models.AutoField(
        primary_key=True
    )
    category_name: models.CharField = models.CharField(
        max_length=100,
        unique=True,
    )
    category_description: models.TextField = models.TextField(
        blank=True,
        null=True
    )
    is_active: models.BooleanField = models.BooleanField(
        default=True
    )
    category_image: models.TextField = models.TextField(
        null=True,
        blank=True
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True
    )

    organisation: models.ForeignKey = models.ForeignKey(
        Organisation,
        on_delete=models.DO_NOTHING,
        related_name="product_categories",
    )

    def __str__(self):
        return self.category_name


class ProductSubcategory(models.Model):
    class Meta:
        verbose_name_plural = "product_subcategories"

    id: models.AutoField = models.AutoField(
        primary_key=True,
    )
    is_active: models.BooleanField = models.BooleanField(
        default=True
    )
    subcategory_name: models.CharField = models.CharField(
        max_length=100
    )
    subcategory_description: models.TextField = models.TextField(
        blank=True,
        null=True
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True
    )

    organisation: models.ForeignKey = models.ForeignKey(
        Organisation,
        on_delete=models.DO_NOTHING,
        default=1
    )
    category: models.ForeignKey = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='product_subcategories',
    )
    category_name: models.TextField = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    class Meta:
        ordering = [ '-created_at' ]

    id: models.AutoField = models.AutoField(
        primary_key=True
    )
    is_active: models.BooleanField = models.BooleanField(
        default=True
    )
    product_name: models.CharField = models.CharField(
        max_length=255,
        unique=True,
    )
    product_description: models.TextField = models.TextField(
        blank=True,
        null=True
    )
    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    discount_price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    unit: models.CharField = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    stock_quantity: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0
    )
    mfg: models.DateField = models.DateField(
        default=date.today
    )
    product_life: models.PositiveIntegerField = models.PositiveIntegerField(
        default=1
    )
    product_image1: models.TextField = models.TextField(
        blank=True,
        null=True
    )
    product_image2: models.TextField = models.TextField(
        blank=True,
        null=True
    )
    availability: models.BooleanField = models.BooleanField(
        default=True
    )
    product_type: models.CharField = models.CharField(
        max_length=20,
        choices=[
            ('veg', 'Vegetarian'),
            ('nonveg', 'Non-Vegetarian'),
            ('organic', 'Organic'),
            ('non-organic', 'Non-Organic')
        ],
        default='organic'
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True
    )

    organisation: models.ForeignKey = models.ForeignKey(
        Organisation,
        on_delete=models.DO_NOTHING,
        related_name="products",
        default=1
    )
    category: models.ForeignKey = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='products',
        default=1
    )
    subcategory: models.ForeignKey = models.ForeignKey(
        ProductSubcategory,
        on_delete=models.CASCADE,
        related_name='products',
        default=1
    )
    # TODO: Fix this logic here. I had a hard time with serializers
    # So I redundandly created the fields below.
    category_name: models.TextField = models.TextField(
        blank=True,
        null=True
    )
    subcategory_name: models.TextField = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.product_name
