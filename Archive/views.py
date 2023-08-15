from django.shortcuts import render
from profiles.models import Profile
from Record.models import Record
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from django.conf import settings
from profiles.serializers import ProfileSerializer
from Record.serializers import RecordSerializer



#1. 친구 목록 불러오는 기능
class BuddyListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    #1-1. 친구 리스트 불러와 List로
    def list(self, request, profile_id=None):
        profile = get_object_or_404(Profile, id=profile_id)
        queryset = self.filter_queryset(self.get_queryset().filter(profile=profile))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

#2. Record 스크랩 불러오는 기능
class RecordListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    #2-1. 스크랩 한 Record 필터링 --> data 가져오기
    @action(detail=False, methods=['GET'])
    def scrap_list(self, request):
        user = request.user
        scrap_list = Record.objects.filter(record_scrap=user)

        serializer = self.get_serializer(scrap_list, many=True)
        return Response(serializer.data)