import requests

from json.decoder import JSONDecodeError

from rest_framework import status
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .authentication import CookieAuthentication


from django.shortcuts import redirect
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login
from django.http import JsonResponse
from .models import User

BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/login/callback/'

state = getattr(settings, 'STATE')


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code') 

    # 1. 받은 인가 코드를 통해 google access token 요청 
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()

    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    
    access_token = token_req_json.get('access_token')


    # 2. 받은 access_token으로 googel에 eamil 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    #
    try:
        # 전달 받은 이메일이 User에 있는지 확인
        user = User.objects.get(email=email)
        isPlus = False
        print("isplus", isPlus)
        # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
        social_user = SocialAccount.objects.get(user=user)

        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}

        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        
        # accept_json = accept.json()
        # accept_json.pop('user', None)
    # User 안에 없으면
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        isPlus = True
        print("isplus", isPlus)
        # 문제 있으면
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        
        # uid = email_req_json.get('user_id')
        # nickname = 'google_'+ str(uid)
        # user = User.objects.get(email=email)
        # user.save()
        

        # accept_json = accept.json()
        # accept_json.pop('user', None)

    user = User.objects.get(email=email)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # login(request, user)

    if isPlus:
        print("True")
        redirect_uri = 'http://127.0.0.1:5173/input'
    else:
        print("false")
        redirect_uri = 'http://127.0.0.1:5173'


    response = redirect(redirect_uri)
    response.set_cookie('access_token', access_token, max_age=3600, httponly=True)

    return response

    # res = {
    #     "detail": "로그인 성공!",
    #     "access": access_token,
    #     "refresh": str(refresh),
    #     "isPlus": isPlus
    # }
    
class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
