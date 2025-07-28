from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

from .models import Customer
from .serializers import (
    CustomerRegistrationSerializer,
    CustomerLoginSerializer,
    CustomerDetailSerializer,  # ✅ make sure this is defined in your serializers
)


# 🔹 Customer Registration API
class CustomerRegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Customer registered successfully",
                "customer_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Customer Login API
class CustomerLoginAPIView(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data.get('mobile_number')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=mobile_number, password=password)
            if user is not None:
                login(request, user)
                return Response({
                    "message": "Login successful",
                    "customer_id": user.id
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid mobile number or password"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Customer Profile API
class CustomerProfileAPIView(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerDetailSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.generics import ListAPIView

# 🔹 View to list all customers (optional/admin)
class CustomerListView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer
