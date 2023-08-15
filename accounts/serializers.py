from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'nickname', 'country', 'city', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'nickname', 'country', 'city', 'profile_img'] # followings 나중에 추가

class SocialUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'nickname', 'country', 'city']