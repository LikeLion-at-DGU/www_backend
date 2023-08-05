from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Record.urls')),
=======
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
>>>>>>> 7caececa06d6345b85f04aa31409566828b564eb
]
