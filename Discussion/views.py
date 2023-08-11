from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action


from .models import Discussion, Choice, DComment
from .serializers import DiscussionSerializer, DCommentSerializer, ChoiceSerializer

# Create your views here.
class DiscussionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer

    # def get_queryset(self):
    #     discussion = self.kwargs.get('dicussion_id')
    #     queryset = Discussion.objects.filter(discussion_id = discussion)
    #     return queryset
class DiscussionChoiceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = ChoiceSerializer
    def get_queryset(self):
        discussion = self.kwargs.get('discussion_id')
        queryset = Choice.objects.filter(discussion_id = discussion)
        return queryset
    
    # 투표하기 기능
    # 같은 discussion 내에 다른 항목에 투표하면 투표되어있던 항목에서는 user 뺴고 count 빼고
    @action(methods=['GET'], detail=True)
    def vote(self, request, pk=None):
        vote_choice = self.get_object()
        # 투표가 눌려져있는 같은 discussion의 다른 항목 가져오기
        voted_choice = Choice.objects.filter(voted_user = request.user) # 같은 disucssion안에 있는 건 filter를 사용하나? 다른 방법을 사용하나?
        # 투표가 눌러져있던 항목에서는 투표수를 줄이고 user를 제외
        voted_choice.cnt -= 1
        voted_choice.voted_user.remove(request.user)
        voted_choice.save()
        # 새로 누른 항목에는 투푯수 증가, user 추가
        voted_choice.cnt += 1
        voted_choice.voted_user.add(request.user)
        voted_choice.save()

        return Response()
        # if request.user in voted_choice.voted_user.all():
            


class DiscussionCommentViewSet(viewsets.ModelViewSet):
    serializer_class = DCommentSerializer
    def get_queryset(self):
        discussion = self.kwargs.get('discussion_id')
        queryset = DComment.objects.filter(discussion_id = discussion)
        return queryset
