from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Companion, CoComment
from .serializers import CompanionSerializer, CoCommentSerializer
from accounts.models import User

# companion
class CompanionViewSet(viewsets.ModelViewSet):
    queryset = Companion.objects.all()
    serializer_class = CompanionSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['country']
    filterset_fields = ['continent']

    def perform_create(self, serializer):
        print('perform', self.request.user)
        serializer.save(writer = self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 여기서 필요한 필드들을 설정하고 저장합니다.
            # print(request.user)
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # companion 게시글 좋아요 
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        like_companion = self.get_object()
        if request.user in like_companion.like.all():
            like_companion.like_count -= 1
            like_companion.like.remove(request.user.id)
        else:
            like_companion.like_count += 1
            like_companion.like.add(request.user.id)

        like_companion.save(update_fields=["like_count"])

        return Response()
    
    # 스크랩 기능
    @action(methods=['POST'], detail=True)
    def scrap(self, request, pk=None):
        scarp_companion = self.get_object()
        if request.user in scarp_companion.scraped_user.all():
            scarp_companion.scraped_user.remove(request.user)
        else:
            scarp_companion.scraped_user.add(request.user)

        scarp_companion.save()
        
        return Response()
    
    @action(methods=['POST'], detail=True)
    def save(self, request, pk=None):
        save_companion = self.get_object()
        save_companion.isSave = True
        save_companion.save(update_fields=['isSave'])

        return Response()

    # 조회수
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

# Comapnion comment - 리스트, 생성
class CompanionCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = CoCommentSerializer
    def get_queryset(self):
        companion = self.kwargs.get('companion_id')
        queryset = CoComment.objects.filter(companion_id = companion)
        return queryset
    
    def create(self, request, companion_id=None):
        companion = get_object_or_404(Companion, id=companion_id)

        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save(companion=companion, writer=request.user)
        return Response(serializer.data)

# comment - 수정, 삭제, 상세
class CommentViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = CoCommentSerializer
    queryset = CoComment.objects.all()
    
    # comment 좋아요
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        like_comment = self.get_object()
        
        if request.user in like_comment.like.all():
            like_comment.like_count -= 1
            like_comment.like.remove(request.user)
        else:
            like_comment.like_count += 1
            like_comment.like.add(request.user)

        like_comment.save(update_fields=["like_count"])

        return Response()

    # 댓글을 통한 follow
    @action(methods=['POST'], detail=True)
    def follow(self, request, pk=None):
        # 현재 로그인한 사용자
        current_user = request.user
        # 팔로우 받는 사용자
        comment_writer = CoComment.objects.get(pk=pk).writer

        # 친구 추가
        current_user.friends.add(comment_writer)
        comment_writer.friends.add(current_user)

        return Response()


