from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Companion, CoComment
from .serializers import CompanionSerializer, CoCommentSerializer

# Create your views here.
class CompanionViewSet(viewsets.ModelViewSet):
    queryset = Companion.objects.all()
    serializer_class = CompanionSerializer

    @action(methods=['GET'], detail=True)
    def like(self, request, pk=None):
        like_companion = self.get_object()
        if request.user in like_companion.like.all():
            like_companion.like_count -= 1
            like_companion.like.remove(request.user)
        else:
            like_companion.like_count += 1
            like_companion.like.add(request.user)

        like_companion.save(update_fields=["like_count"])

        return Response()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    # def update_comments_count(self, instance):
    #     instance.comments_count = instance.comments.count()
    #     instance.save()

class CompanionCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CoCommentSerializer
    def get_queryset(self):
        companion = self.kwargs.get('companion_id')
        queryset = CoComment.objects.filter(companion_id = companion)
        return queryset
    
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        print(pk, "pk")
        like_comment = self.get_object()
        
        if request.user in like_comment.like.all():
            like_comment.like_count -= 1
            like_comment.like.remove(request.user)
        else:
            like_comment.like_count += 1
            like_comment.like.add(request.user)

        like_comment.save(update_fields=["like_count"])

        return Response()