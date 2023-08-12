from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import CompanionViewSet, CompanionCommentViewSet, CommentViewSet

app_name = "companion"

companion_router = routers.SimpleRouter()
companion_router.register('companions', CompanionViewSet, basename='companions')

companion_comment_router = routers.SimpleRouter()
companion_comment_router.register('cocomments', CompanionCommentViewSet, basename='cocomments')

comment_router = routers.SimpleRouter()
comment_router.register('cocomments', CommentViewSet, basename='cocomments')

urlpatterns = [
    path('', include(companion_router.urls)),
    path('companions/<int:companion_id>/', include(companion_comment_router.urls)),
    path('', include(comment_router.urls)),
]