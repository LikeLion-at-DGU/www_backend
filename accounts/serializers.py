from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    
    friendsCount = serializers.SerializerMethodField()
    def get_friendsCount(self, instance):
        return instance.friends.count()

    class Meta:
        model = User
        fields = ['email', 'nickname', 'country', 'city', 'profile_img', 'friend', 'friendsCount'] # followings 나중에 추가

# class SocialUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['email', 'nickname', 'country', 'city']

class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh_token'])
        data = {'access_token': str(refresh.access_token)}

        return data


# class UserRegisterSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['email', 'nickname', 'country', 'city', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

# class UserLoginSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}