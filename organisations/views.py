from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organisation
from .serializers import OrganisationSerializer
from django.shortcuts import get_object_or_404

class OrganisationAPIView(APIView):
    def get(self, request, id=None):
        if id:
            organisation = get_object_or_404(Organisation, id=id)
            serializer = OrganisationSerializer(organisation)
            return Response(serializer.data)
        organisations = Organisation.objects.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        organisation = get_object_or_404(Organisation, id=id)
        serializer = OrganisationSerializer(organisation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        organisation = get_object_or_404(Organisation, id=id)
        serializer = OrganisationSerializer(organisation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            org = Organisation.objects.get(id=id)
            org.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Organisation.DoesNotExist:
            return Response({'error': 'Organisation not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
