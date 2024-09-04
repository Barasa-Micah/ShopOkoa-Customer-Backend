from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import UserSerializer, UserSerializerWithToken, ProfileSerializer
from rest_framework import generics
from rest_framework import permissions
from users.models import Profile
import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework.request import Request
import datetime
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema

# Google Auth imports
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView



class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user

# Create your views here.

class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetail(generics.RetrieveDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @swagger_auto_schema(operation_summary="Retrieve a Profile", operation_description="Retrieve a Profile")
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary="Update a Profile", operation_description="Update a Profile")
    def put(self, request: Request, *args, **kwargs) -> Response:
        pk = kwargs['pk']
        profile = self.queryset.get(pk=pk)

        if profile and profile.user == self.request.user:
            serializer = self.serializer_class(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(operation_summary="Delete a Profile", operation_description="Delete a Profile")
    def delete(self, request: Request, *args, **kwargs) -> Response:
        pk = kwargs['pk']
        profile = self.queryset.get(pk=pk)

        if profile and profile.user == self.request.user:
            profile.delete()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)


class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @swagger_auto_schema(operation_summary="Retrieve authorized User's detail", operation_description="Retrieve authorized User's detail")
    def get(self, request: Request, *args, **kwargs) -> Response:
        user = self.queryset.get(pk=request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Update a User", operation_description="Update a User")
    def put(self, request: Request, *args, **kwargs) -> Response:
        pk = kwargs['pk']
        user = self.queryset.get(pk=pk)

        if user:
            serializer = self.serializer_class(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(operation_summary="Delete a User", operation_description="Delete a User")
    def delete(self, request: Request, *args, **kwargs) -> Response:
        pk = kwargs['pk']
        user = self.queryset.get(pk=pk)

        if user:
            user.delete()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)

    
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:8000/api/v1/auth/google/callback/"