from django.urls import path, include
from .oauth import *
from .views import *
from rest_framework import routers

app_name = "accounts"

# user_routers = routers.SimpleRouter()
# user_routers.register('users', UserViewset, basename='users')


urlpatterns = [
    # 구글
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    # 구글 로그인 후 정보 저장 
    path('save_user', SocialSignUpViewset.as_view(), name='save_user'),
    # user
    path('profile', UserViewset.as_view(), name='profile'),
    # path('userprofile', MyProfileViewset, name="userprofile"),
]
