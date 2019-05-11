from django.contrib import admin
from django.urls import path

from .views import Contact

urlpatterns = [
    path('contact/', Contact, name='contact'),
]