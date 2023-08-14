from .models import Record, RComment, Card, Tag, Upload_image
from .serializers import RecordSerializer, RecordListSerializer, RCommentSerializer, CardSerializer, Upload_imageSerializer
from profiles.models import Profile # 프로필 앱에서 프로필 모델 import 하기
from accounts.models import User


from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

#1. RECORD 글 작성 기능
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    def get_serializer_class(self):
        if self.action == "list":
            return RecordListSerializer
        return RecordSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'body']
    
    #1-1. 태그 작성
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        record = serializer.instance
        
        # self.handle_tags(record)

        return Response(serializer.data)
    
    # 1-2. 태그 작성 (2)
    # def handle_tags(self, record):
    #     words = record.body.split(' ')
    #     tag_list = []
    #     for w in words:
    #         if w[0] == '#':
    #             tag_list.append(w[1:])

    #     for t in tag_list:
    #         tag, created = Tag.objects.get_or_create(name=t)
    #         record.tag.add(tag)

    #     record.save()

    #1-3. 수정 함수 구현
    def perform_update(self, serializer):
        record = serializer.save()
        record.tag.clear()
        self.handle_tags(record)

    #1-4. 좋아요 기능 구현 (요청마다 views 필드 수정하기)
    @action(methods=["GET"], detail=True)
    def record_like(self, request, pk=None):
        like_record = self.get_object()
        like_record.likes += 1
        like_record.save(update_fields=["likes"])
        return Response()
    
    #1-5. 조회수 기능 (views)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    #1-6. 스크랩 기능
    @action(methods=['POST'], detail=True)
    def record_scrap(self, request, pk=None):
        scrap_record = self.get_object()
        if request.user in scrap_record.record_scrap.all():
            scrap_record.record_scrap.remove(request.user)
        else:
            scrap_record.record_scrap.add(request.user)
            
        scrap_record.save()
        return Response()


#2. RComment 디테일 조회 수정 삭제 기능
class RCommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = RComment.objects.all()
    serializer_class = RCommentSerializer



#3. Record 글에 있는 댓글 목록 조회, Record 게시물에 댓글 작성
class RecordRCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = RComment.objects.all()
    serializer_class = RCommentSerializer

    def list(self, request, record_id=None):
        record = get_object_or_404(Record, id=record_id)
        queryset = self.filter_queryset(self.get_queryset().filter(record=record))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, record_id=None):
        record = get_object_or_404(Record, id=record_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(record=record)
        return Response(serializer.data)
    
    #3-1. 댓글을 통한 유저 follow (댓글 id 값 들어가서 팔로우 수행)
    @action(detail=True, methods=['GET'])
    def follow(self, request, record_id=None, pk=None):
        
        user=request.user # user = 요청한 유저
        # 파라미터로 받은 id에 해당하는 객체를 User 모델에서 가져온다
        followed_user=get_object_or_404(User, pk=followed_user.id)
        # 팔로우 한 사람들 리스트에 요청한 유저가 있는지 확인
        is_follower=user.profile in followed_user.profile.followers.all()
        if is_follower: # 있다면, followed_user를 팔로잉 목록에서 지운다
            user.profile.followings.remove(followed_user.profile)
        else: # 아니라면, followed_user를 팔로잉 목록에 추가한다
            user.profile.followings.add(followed_user.profile)
        
        return Response()


#4. Record와 연결된 Card 목록 조회, Card 작성
class CardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    # 아래 코드는 댓글이랑 똑같...음...왤까??? 이게 맞나????
    def list(self, request, record_id=None):
        record = get_object_or_404(Record, id=record_id)
        queryset = self.filter_queryset(self.get_queryset().filter(record=record))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    #4-1. create
    def create(self, request, record_id=None):
        record = get_object_or_404(Record, id=record_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(record=record)

        # 태그 작성 (1)
        self.perform_create(serializer)

        card = serializer.instance
        self.handle_tags(card)

        return Response(serializer.data)
    
    #4-2. 태그 작성(2)
    def handle_tags(self, card):
        words = card.tag_field.split(' ')
        tag_list = []
        for w in words:
            if w[0] == '#':
                tag_list.append(w[1:])

        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name=t)
            card.tag.add(tag)

        card.save()

    #4-3. Card 스크랩 기능
    @action(methods=['POST'], detail=True)
    def card_scrap(self, request, record_id=None, pk=None):
        scrap_card = self.get_object()
        if request.user in scrap_card.card_scrap.all():
            scrap_card.card_scrap.remove(request.user)
        else:
            scrap_card.card_scrap.add(request.user)
            
        scrap_card.save()
        return Response()
    

#5. 이미지 URL을 관리
class Upload_imageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Upload_image.objects.all()
    serializer_class = Upload_imageSerializer