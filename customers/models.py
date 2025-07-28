from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from organisations.models import Organisation


# ------------------------------
# Custom user manager
# ------------------------------
class CustomerManager(BaseUserManager):
    def create_user(self, mobile_number: str, password: str | None = None, **extra_fields: Any):
        """
        Creates and saves a Customer with the given mobile number and password.
        """
        if not mobile_number:
            raise ValueError("The mobile number must be set")
        
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number: str, password: str, **extra_fields: Any):
        """
        Creates and saves a superuser with the given mobile number and password.
        """
        extra_fields.setdefault('is_super_admin', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)  # Required by Django admin if we add it later

        # 👇 Default organisation for superuser, adjust pk if needed
        extra_fields.setdefault('organisation', Organisation.objects.get(pk=1))

        return self.create_user(mobile_number, password, **extra_fields)


# ------------------------------
# Custom Customer model
# ------------------------------
class Customer(AbstractBaseUser):
    # Authentication setup
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Manager
    objects = CustomerManager()

    # Core fields
    id = models.AutoField(primary_key=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=100)

    # Personal info
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)

    # Billing addresses
    billing_address = models.TextField(null=True, blank=True)
    billing_address_specifier = models.TextField(null=True, blank=True)
    billing_address2 = models.TextField(null=True, blank=True)
    billing_address2_specifier = models.TextField(null=True, blank=True)

    # Location info
    country = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)

    # Status flags
    is_active = models.BooleanField(default=True)
    is_super_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Linked organisation
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.DO_NOTHING,
        related_name="customers",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.mobile_number})"


# ------------------------------
# Customer Log Model
# ------------------------------
class CustomerLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    transaction_name = models.CharField(max_length=500)
    mode = models.CharField(max_length=100)  # E.g., POST, PATCH, etc.
    log_message = models.TextField()

    user = models.ForeignKey(
        "Customer",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="log_Customer_id",
    )

    is_app = models.BooleanField(default=False)
    log_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_name
