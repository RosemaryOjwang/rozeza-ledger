from django.urls import path

from .views import company_selection

urlpatterns = [
    path("companies/", company_selection, name="company_selection"),
]