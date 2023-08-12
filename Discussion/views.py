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
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    
    # 투표하기 기능
    # 같은 discussion 내에 다른 항목에 투표하면 투표되어있던 항목에서는 user 뺴고 count 빼고
    @action(methods=['POST'], detail=True)
    def vote(self, request, pk=None):
        choice = self.get_object()
        print(choice, "choice")
        # 현재 choice의 discussion 가져오기
        discussion = Discussion.objects.get(choices = choice)
        print(discussion, "discussion")

        try:
            voted_choice = Choice.objects.get(discussion=discussion, voted_user = request.user) # 같은 disucssion안에 있는 건 filter를 사용하나? 다른 방법을 사용하나?
        except:
            voted_choice = None
        print(voted_choice, "voted_choice")

        print(voted_choice.cnt)
        if voted_choice:
            # 투표가 눌러져있던 항목에서는 투표수를 줄이고 user를 제외
            voted_choice.cnt -= 1
            voted_choice.voted_user.remove(request.user)
            voted_choice.save()
            # 새로 누른 항목에는 투표수 증가, user 추가
            choice.cnt += 1
            choice.voted_user.add(request.user)
            choice.save()
        else: 
            choice.cnt += 1
            choice.voted_user.add(request.user)
            choice.save()

        return Response()
        # if request.user in voted_choice.voted_user.all():
            
class DiscussionCommentViewSet(viewsets.ModelViewSet):
    serializer_class = DCommentSerializer
    def get_queryset(self):
        discussion = self.kwargs.get('discussion_id')
        queryset = DComment.objects.filter(discussion_id = discussion)
        return queryset
