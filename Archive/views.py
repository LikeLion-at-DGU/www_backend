from django.shortcuts import render
from profiles.models import Profile
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from django.conf import settings
from profiles.serializers import ProfileSerializer



#1. 친구 목록 불러오는 기능
class BuddyListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    #1-1. 친구 리스트 불러와 List 로
    def list(self, request, profile_id=None):
        profile = get_object_or_404(Profile, id=profile_id)
        queryset = self.filter_queryset(self.get_queryset().filter(profile=profile))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)