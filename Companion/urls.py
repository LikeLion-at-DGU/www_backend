from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import CompanionViewSet, CompanionCommentViewSet

app_name = "companion"

companion_router = routers.SimpleRouter()
companion_router.register('companions', CompanionViewSet, basename='companions')

companion_comment_router = routers.SimpleRouter()
companion_comment_router.register('comments', CompanionCommentViewSet, basename='comments')

urlpatterns = [
    path('', include(companion_router.urls)),
    path('companions/<int:companion_id>/', include(companion_comment_router.urls)),
]