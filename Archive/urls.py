from django.urls import path, include
from rest_framework import routers
from .views import BuddyListViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = "Archive"

#1. 친구 목록 불러오는 기능
BuddyList_router = routers.SimpleRouter()
BuddyList_router.register("list", BuddyListViewSet, basename="list")


urlpatterns = [
    path("", include(BuddyList_router.urls)), #1. 친구 목록 불러오는 기능

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)