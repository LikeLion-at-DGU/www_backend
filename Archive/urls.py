from django.urls import path, include
from rest_framework import routers
from .views import BuddyListViewSet, RecordListViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = "Archive"

#1. 친구 목록 불러오는 기능
BuddyList_router = routers.SimpleRouter()
BuddyList_router.register("list", BuddyListViewSet, basename="list")

#2. Record 스크랩 불러오는 기능
RecordList_router = routers.SimpleRouter()
RecordList_router.register("recordlist", RecordListViewSet, basename="recordlist")


urlpatterns = [
    path("", include(BuddyList_router.urls)), #1. 친구 목록 불러오는 기능
    path("", include(RecordList_router.urls)), #2. Record 스크랩 불러오는 기능
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)