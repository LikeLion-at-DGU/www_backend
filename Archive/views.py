from django.shortcuts import render
from Companion.models import Companion
from Record.models import Record
from accounts.models import User
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from django.conf import settings
from Record.serializers import RecordSerializer, CardSerializer
from Companion.serializers import CompanionSerializer
from accounts.serializers import UserSerializer


#1. 친구 목록 불러오는 기능




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
    queryset = Record.objects.all()
    serializer_class = CardSerializer

    #4-1. 스크랩 한 Card 필터링 --> data 가져오기
    @action(detail=False, methods=['GET'])
    def scrap_list(self, request):
        user = request.user
        scrap_list = Record.objects.filter(card_scrap=user)

        serializer = self.get_serializer(scrap_list, many=True)
        return Response(serializer.data)




#5. 내가 쓴 글 불러오는 기능 (아직...안됨....)
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
    

#6. 내 친구들 불러오는 기능
class FriendsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def get_friends(self, request):
        current_user = request.user
        if current_user.friend:
            friends = current_user.friend.all()  # 해당 사용자의 모든 친구 불러오기

        # 친구들의 정보를 원하는 형식으로 가공
        friends_data = []
        for friend in friends:
            friends_data.append({
                'nickname': friend.nickname,
                'country': friend.country,
                'city': friend.city,
            })