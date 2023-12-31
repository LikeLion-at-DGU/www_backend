from django.urls import path, include
from rest_framework import routers
from .views import RecordViewSet, RCommentViewSet, RecordRCommentViewSet, Upload_imageViewSet, CardViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = "Record"

#1. RECORD 글 작성
record_router = routers.SimpleRouter()
record_router.register("records", RecordViewSet, basename="record")

#2. RComment 디테일 조회 수정 삭제
rcomment_router = routers.SimpleRouter()
rcomment_router.register("rcomments", RCommentViewSet, basename="rcomments")

#3. Record 게시물에 있는 댓글 목록 조회, 게시물에 댓글 작성
record_rcomment_router = routers.SimpleRouter()
record_rcomment_router.register("rcomments", RecordRCommentViewSet, basename="rcomments")

#4. Upload_image
upload_image_router = routers.SimpleRouter()
upload_image_router.register("upload_image", Upload_imageViewSet, basename="upload_image")

#5. Card
card_router = routers.SimpleRouter()
card_router.register("card", CardViewSet, basename="CardViewSet")


urlpatterns = [
    path("", include(record_router.urls)), #1. RECORD 글 작성
    path("", include(rcomment_router.urls)), #2. RComment 디테일 조회 수정 삭제
    path("records/<int:record_id>/", include(record_rcomment_router.urls)), #3. Record 게시물에 있는 댓글 목록 조회, 게시물에 댓글 작성
    path("", include(upload_image_router.urls)), #4. Upload_image
    path("", include(card_router.urls)), #5. Card
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)