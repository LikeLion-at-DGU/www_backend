from django.urls import path, include
from rest_framework import routers
from .views import RecordListViewSet, CompanionListViewSet, MyRecordViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = "Archive"

#1. 친구 목록 불러오는 기능


#2. Record 스크랩 불러오는 기능
RecordList_router = routers.SimpleRouter()
RecordList_router.register("recordlist", RecordListViewSet, basename="recordlist")

#3. Companions 스크랩 불러오는 기능
CompanionList_router = routers.SimpleRouter()
CompanionList_router.register("companionlist", CompanionListViewSet, basename="companionlist")

#5. 내가 쓴 Record 글 불러오는 기능
MyList_router = routers.SimpleRouter()
MyList_router.register("myrecord", MyRecordViewSet, basename="myrecord")



urlpatterns = [
    path("", include(RecordList_router.urls)), #2. Record 스크랩 불러오는 기능
    path("", include(CompanionList_router.urls)), #3. Companions 스크랩 불러오는 기능
    path("", include(MyList_router.urls)), #5. 내가 쓴 Record 글 불러오는 기능

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)