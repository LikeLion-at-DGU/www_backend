from .models import Record, RComment, Tag, Upload_image
from .serializers import RecordSerializer, RecordListSerializer, RCommentSerializer, Upload_imageSerializer, CardSerializer
from accounts.models import User

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from urllib.parse import unquote
from rest_framework.parsers import MultiPartParser


#1. RECORD 글 작성 기능
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "body", "=tag__name"]

    def get_serializer_class(self):
        if self.action == "list":
            return RecordListSerializer
        return RecordSerializer
    

    #1-0. 검색처리 (띄어쓰기 가능)
    def get_queryset(self):
        search_query = self.request.query_params.get('search')
        if search_query:
            decoded_query = unquote(search_query)
            # Compare the decoded_query with available fields
            available_fields = ["title", "body", "tag__name"]
            if decoded_query in available_fields:
                self.search_fields += [decoded_query]
        return super().get_queryset()
    
    parser_classes = [MultiPartParser]
    # 필요한 곳에만 parser_classes를 MultiPartParser로 설정

    #1-1. 태그 작성
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        record = serializer.instance
        
        self.handle_tags(record)

        return Response(serializer.data)
    

    #1-3. 수정 함수 구현
    def perform_update(self, serializer):
        record = serializer.save()
        record.tag.clear()
        self.handle_tags(record)

    #1-4. 좋아요 기능 구현
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        like_record = self.get_object()
        if request.user in like_record.rlike.all():
            like_record.rlike_count -= 1
            like_record.rlike.remove(request.user)
        else:
            like_record.rlike_count += 1
            like_record.rlike.add(request.user)

        like_record.save(update_fields=["rlike_count"])

        return Response()
    
    #1-5. 조회수 기능 (views)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    #1-6. Record 스크랩 기능
    @action(methods=['POST'], detail=True)
    def record_scrap(self, request, pk=None):
        scrap_record = self.get_object()
        if request.user in scrap_record.record_scrap.all():
            scrap_record.record_scrap.remove(request.user)
        else:
            scrap_record.record_scrap.add(request.user)
            
        scrap_record.save()
        return Response()
    
    #1-7. 카드 태그 기능
    def handle_tags(self, record):
        words = record.tag_field.split(' ')
        tag_list = []
        for w in words:
            if w[0] == '#':
                tag_list.append(w[1:])

        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name=t)
            record.tag.add(tag)

        record.save()

    # #1-8. Card 스크랩 기능
    # @action(methods=['POST'], detail=True)
    # def card_scrap(self, request, pk=None):
    #     scrap_card = self.get_object()
    #     if request.user in scrap_card.card_scrap.all():
    #         scrap_card.card_scrap.remove(request.user)
    #     else:
    #         scrap_card.card_scrap.add(request.user)
    
    #     scrap_card.save()
    #     return Response()


#2. RComment 디테일 조회 수정 삭제 기능
class RCommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = RComment.objects.all()
    serializer_class = RCommentSerializer

    #2-1. comment 좋아요
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        like_comment = self.get_object()
        
        if request.user in like_comment.rcomment_like.all():
            like_comment.rcomment_like_count -= 1
            like_comment.rcomment_like.remove(request.user)
        else:
            like_comment.rcomment_like_count += 1
            like_comment.rcomment_like.add(request.user)

        like_comment.save(update_fields=["rcomment_like_count"])

        return Response()
    
    





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
        serializer.save(record=record, writer=request.user)
        return Response(serializer.data)
    


    #3-1. 댓글을 통한 follow (Profile 모델을 통한 팔로우)
    @action(methods=['POST'], detail=True)
    def follow2(self, request, pk=None, record_id=None):
        # 현재 로그인 한 사용자
        user = request.user
        # 팔로우 받는 사용자
        followed_user = RComment.objects.get(pk=pk).writer

        is_follower = user.profile in followed_user.profile.followings.all()
        
        # 친구 추가
        if is_follower:
            user.profile.followings.remove(followed_user.profile)
        else:
            user.profile.followings.add(followed_user.profile)
        return Response()




#4. 이미지 URL을 관리
class Upload_imageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Upload_image.objects.all()
    serializer_class = Upload_imageSerializer


#5. Card 관리
class CardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Record.objects.all()
    serializer_class = CardSerializer

    # Card 검색 (태그)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["=tag__name"]

    #5-1. Card 스크랩 기능
    @action(methods=['POST'], detail=True)
    def card_scrap(self, request, pk=None):
        scrap_card = self.get_object()
        if request.user in scrap_card.card_scrap.all():
            scrap_card.card_scrap.remove(request.user)
        else:
            scrap_card.card_scrap.add(request.user)
            
        scrap_card.save()
        return Response()