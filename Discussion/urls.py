from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import DiscussionViewSet, DiscussionCommentViewSet, DiscussionChoiceViewSet

app_name = "dicussion"

# discussion CRUD router
dicussion_router = routers.SimpleRouter()
dicussion_router.register('discussions', DiscussionViewSet, basename="discussions")

# discussion에 대한 comment CRUD router
discsusion_comment_router = routers.SimpleRouter()
discsusion_comment_router.register('comments', DiscussionCommentViewSet, basename="comments")

# discussion에 대한 투표 항목
discussion_choice_router = routers.SimpleRouter()
discussion_choice_router.register('choices', DiscussionChoiceViewSet, basename="choices")


urlpatterns = [
    path('', include(dicussion_router.urls)),
    path('discussions/<int:discussion_id>/', include(discsusion_comment_router.urls)),
    path('discussions/<int:discussion_id>/', include(discussion_choice_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)