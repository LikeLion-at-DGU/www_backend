from django.shortcuts import render
from profiles.models import Profile
from Companion.models import Companion
from Record.models import Record, Card
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from django.conf import settings
from profiles.serializers import ProfileSerializer
from Record.serializers import RecordSerializer, CardSerializer
from Companion.serializers import CompanionSerializer



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
    


#3. Companion 스크랩 불러오는 기능
class CompanionListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Companion.objects.all()
    serializer_class = CompanionSerializer

    #3-1. 스크랩 한 Companion 필터링 --> data 가져오기
    @action(detail=False, methods=['GET'])
    def scrap_list(self, request):
        user = request.user
        scrap_list = Companion.objects.filter(scraped_user=user)

        serializer = self.get_serializer(scrap_list, many=True)
        return Response(serializer.data)
    

#4. Card 스크랩 불러오는 기능
class CardListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    #4-1. 스크랩 한 Card 필터링 --> data 가져오기
    @action(detail=False, methods=['GET'])
    def scrap_list(self, request):
        user = request.user
        scrap_list = Card.objects.filter(card_scrap=user)

        serializer = self.get_serializer(scrap_list, many=True)
        return Response(serializer.data)
    

#5. 내가 쓴 글 불러오는 기능
class MyRecordViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    #5-1. 본인이 쓴 Record 글 필터링 --> data 가져오기
    @action(detail=False, methods=['GET'])
    def my_list(self, request):
        user = request.user
        my_records = Record.objects.filter(writer=user)

        serializer = self.get_serializer(my_records, many=True)
        return Response(serializer.data)