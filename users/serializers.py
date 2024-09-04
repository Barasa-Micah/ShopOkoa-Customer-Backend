from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
from dj_rest_auth.registration.views import RegisterView
from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class NameRegistrationSerializer(RegisterSerializer):
  first_name = serializers.CharField(required=False)
  last_name = serializers.CharField(required=False)

  def custom_signup(self, request, user):
    user.first_name = self.validated_data.get('first_name', '')
    user.last_name = self.validated_data.get('last_name', '')
    user.save(update_fields=['first_name', 'last_name'])

class NameRegistrationView(RegisterView):
  serializer_class = NameRegistrationSerializer


class UserSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
            'last_name', 'email']
    def get_id(self, obj):
            return obj.id
    def get_isAdmin(self, obj):
        return obj.is_staff
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name    
    

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True, read_only=False)

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        return super().update(instance, validated_data)


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

class CustomPasswordResetSerializer(_PasswordResetSerializer):
   def get_email_options(self):
       return {
           'html_email_template_name': 'registration/custom_reset_confirm.html',
       }
