from django.urls import path, include
from .oauth import *
from .views import *
from rest_framework import routers

app_name = "accounts"

user_routers = routers.SimpleRouter()
user_routers.register('users', UserViewset, basename='users')


urlpatterns = [
    # 구글
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    # 그 외
    path('', include(user_routers.urls)),
    path('save_user', SocialSignUpViewset.as_view(), name='save_user'),
]
