from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

app_name = "profiles"

urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
