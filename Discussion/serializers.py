from rest_framework import serializers
from .models import Discussion, Choice, Comment

class DiscussionSerializer(serializers.ModelSerializer):
    
    comments = serializers.SerializerMethodField()
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    choices = serializers.SerializerMethodField()
    def get_choices(self, instance):
        serializer = ChoiceSerializer(instance.choices, many=True)
        return serializer.data

    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Discussion
        fields = ['id', 'writer', 'created_at','updated_at', 'comments', 'choices']
        read_only = ['id', 'writer', 'created_at', 'updated_at', 'comments']

# Choice serializer가 필요한지 잘 모르겠음
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'
        read_only = ['id', 'discussion', 'count']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields= '__all__'
        read_only = ['id', 'writer', 'discussion', 'created_at', 'updated_at']

