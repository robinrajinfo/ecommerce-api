from django.urls import path
from .views import OrganisationAPIView  

urlpatterns = [
    path('organisations/', OrganisationAPIView.as_view()),  
    path('create-organisation/', OrganisationAPIView.as_view()),
    path('get-organisation/<int:id>/', OrganisationAPIView.as_view()),
    path('update-organisation/<int:id>/', OrganisationAPIView.as_view()),
    path('delete-organisation/<int:id>/', OrganisationAPIView.as_view()),
]
