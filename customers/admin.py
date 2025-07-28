from django.contrib import admin
from .models import Customer, CustomerLog


# ------------------------------
# Admin configuration for Customer
# ------------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'first_name', 
        'last_name', 
        'mobile_number', 
        'email', 
        'is_active', 
        'is_admin',
        'is_super_admin',
        'organisation',
        'created_at'
    )
    search_fields = ('first_name', 'last_name', 'mobile_number', 'email')
    list_filter = ('is_active', 'is_admin', 'is_super_admin', 'organisation')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Fields grouping in admin form
    fieldsets = (
        ("Personal Info", {
            'fields': ('first_name', 'last_name', 'mobile_number', 'email', 'password')
        }),
        ("Address", {
            'fields': (
                'billing_address', 'billing_address_specifier',
                'billing_address2', 'billing_address2_specifier',
                'city', 'state', 'country', 'postal_code',
            )
        }),
        ("Status Flags", {
            'fields': (
                'is_active', 'is_admin', 'is_super_admin', 'is_customer', 'is_staff'
            )
        }),
        ("Organisation & Timestamps", {
            'fields': ('organisation', 'created_at', 'updated_at')
        }),
    )


# ------------------------------
# Admin configuration for CustomerLog
# ------------------------------
@admin.register(CustomerLog)
class CustomerLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transaction_name',
        'mode',
        'user',
        'is_app',
        'log_date'
    )
    search_fields = ('transaction_name', 'log_message')
    list_filter = ('is_app', 'mode')
    ordering = ('-log_date',)
