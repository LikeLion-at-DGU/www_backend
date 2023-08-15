from django.urls import path, include
from .oauth import *
from .views import *
from rest_framework import routers

app_name = "accounts"


urlpatterns = [
    # 구글
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),

    # path('', views.)

    # path('', include(default_router.urls)),
    path('save_user', SocialSignUpViewset.as_view(), name='save_user'),
]
