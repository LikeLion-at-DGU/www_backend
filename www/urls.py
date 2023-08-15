from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Record.urls')),
    path('api/', include('Discussion.urls')),
    path('api/', include('Companion.urls')),
    # accoutns
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
] 
