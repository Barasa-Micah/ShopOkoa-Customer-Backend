from django.urls import path, re_path
from api import views as api_views

urlpatterns = [
    path('', api_views.welcome_to_shopokoa, name='Business Logic'),
]
