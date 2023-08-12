from rest_framework import serializers
from .models import Discussion, Choice, DComment

class DiscussionSerializer(serializers.ModelSerializer):
    
    comments = serializers.SerializerMethodField()
    def get_comments(self, instance):
        serializer = DCommentSerializer(instance.comments, many=True)
        return serializer.data
    
    choices = serializers.SerializerMethodField()
    def get_choices(self, instance):
        serializer = ChoiceSerializer(instance.choices, many=True)
        return serializer.data
    
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Discussion
        fields = ['id', 'title', 'writer', 'created_at','updated_at', 'comments', 'choices', 'image']
        read_only = ['id', 'writer', 'created_at', 'updated_at', 'comments']

# Choice serializer가 필요한지 잘 모르겠음
class ChoiceSerializer(serializers.ModelSerializer):
    
    discussion = serializers.SerializerMethodField()
    def get_discussion(self, instance):
        return instance.discussion.title

    class Meta:
        model = Choice
        fields = ['id', 'discussion', 'vote_item', 'cnt']
        read_only = ['id', 'discussion', 'cnt']
    

class DCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DComment
        fields= '__all__'
        read_only = ['id', 'writer', 'discussion', 'created_at', 'updated_at']

