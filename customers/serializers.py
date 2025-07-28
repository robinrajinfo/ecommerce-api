from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Customer, CustomerLog


# ------------------------------
# General-purpose customer serializer
# ------------------------------
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# ------------------------------
# Dedicated registration serializer
# ------------------------------
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email', 'password', 'mobile_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_mobile_number(self, value):
        if Customer.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already registered.")
        return value

    def create(self, validated_data):
        user = Customer(
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ------------------------------
# Customer login serializer
# ------------------------------
class CustomerLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        mobile_number = data.get("mobile_number")
        password = data.get("password")

        if not mobile_number or not password:
            raise serializers.ValidationError("Both mobile number and password are required.")

        user = authenticate(username=mobile_number, password=password)

        if not user:
            raise serializers.ValidationError("Invalid mobile number or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data["user"] = user
        return data


# ------------------------------
# Limited customer profile details
# ------------------------------
class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'mobile_number', 'email']


# ------------------------------
# Customer activity logging (optional)
# ------------------------------
class CustomerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLog
        fields = '__all__'
