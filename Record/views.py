from .models import Record, RComment, Tag, Card
from .serializers import RecordSerializer, RecordListSerializer, RCommentSerializer, CardSerializer

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action

#1. RECORD 글 작성 기능
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    def get_serializer_class(self):
        if self.action == "list":
            return RecordListSerializer
        return RecordSerializer
    
    #1-1. 태그 작성
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        record = serializer.instance
        self.handle_tags(record)

        return Response(serializer.data)
    
    #1-2. 태그 작성 (2)
    def handle_tags(self, record):
        words = record.body.split(' ')
        tag_list = []
        for w in words:
            if w[0] == '#':
                tag_list.append(w[1:])

        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name=t)
            record.tag.add(tag)

        record.save()

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


#2. RComment 디테일 조회 수정 삭제 기능
class RCommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = RComment.objects.all()
    serializer_class = RCommentSerializer



#3. Record 글에 있는 댓글 목록 조회, Record 게시물에 댓글 작성
class RecordRCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
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
    

    
#4. Record와 연결된 Card 목록 조회, Card 작성
class CardViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    # 아래 코드는 댓글이랑 똑같...음...왤까??? 이게 맞나????
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
