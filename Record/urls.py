from django.urls import path, include
from rest_framework import routers
from .views import RecordViewSet

app_name = "Record"

record_router = routers.SimpleRouter()
record_router.register("records", RecordViewSet, basename="record")

urlpatterns = [
    path("", include(record_router.urls)), # Record 글 url
]