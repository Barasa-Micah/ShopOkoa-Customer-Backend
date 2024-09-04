import datetime
from decouple import config


from django.db.models import Max, Q
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema


from users.models import Profile
from .permissions import IsOwnerOrReadOnly


# Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


def welcome_to_shopokoa(request):
    return HttpResponse("Welcome to ShopOkoa! Your one-stop e-commerce solution.")


# Class-based views