from rest_framework import viewsets, mixins, status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.dispatch import receiver

from .serializers import  UserSerializer
from .models import User, Profile

from .authentication import CookieAuthentication


# 내가 생각하는 viewset
class SocialSignUpViewset(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # user = get_object_or_404(User, pk=pk)
        user = request.user
        user.nickname = request.data.get('nickname')
        user.country = request.data.get('country')
        user.city = request.data.get('city')
        user.save()
            
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        res = Response(
            {
                "message": "회원가입 성공!"
            },
            status=status.HTTP_200_OK,
        )
        return res
    
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewset(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
class FriendViewset(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(user)

class TestLoginViewset(APIView):
    def post(self, request, *args, **kwargs):
        test_email = 'test1@naver.com'
        test_password = '1234'

        user = User.objects.get(email=test_email)
        print(user)
        # user = authenticate(request, email=test_email, password=test_password)
        # print(user)

        if user is not None:
            # 로그인 처리
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            login(request, user)

            res =  Response(
                {
                    "user": {
                        'nickname': user.nickname,
                        'email': user.email,
                        'country' : user.country,
                        'city': user.city,
                        'password' : user.password
                    },
                    "message": "로그인 성공!",
                    "token": {
                        "access": access_token,
                        "refresh": str(refresh),
                    },
                },
                status=status.HTTP_200_OK,
                )
            return res
        
        return Response({"message": "테스트 로그인 실패!"}, status=401)
        
        

# User 모델 생성 할 때, Profile 자동적으로 생성
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

