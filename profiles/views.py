from django.shortcuts import render
from rest_framework import viewsets, mixins
from .serializers import ProfileSerializer
from .models import Profile



#1. 프로필 보는 기능
class ProfileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
