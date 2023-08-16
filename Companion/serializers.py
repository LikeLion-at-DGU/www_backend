from rest_framework import serializers
from .models import Companion, CoComment

class CompanionSerializer(serializers.ModelSerializer):
    
    comments = serializers.SerializerMethodField()
    def get_comments(self, instance):
        serializer = CoCommentSerializer(instance.comments, many=True)
        return serializer.data
    
    comments_count = serializers.SerializerMethodField()
    def get_comments_count(self, instance):
        return instance.comments.count()
    
    # isLike = serializers.SerializerMethodField()
    # def get_isLike(self, instance):
    #     requested_user = self.context.get('requested_user')


    class Meta:
        model = Companion
        fields = ['id','title','writer','body','date','continent','country','city','views','comments','comments_count','like_count', 'isSave', 'created_at']
        read_only = ['id', 'writer', 'views', 'comments_count', 'like_count', 'isSave', 'created_at']
    

class CoCommentSerializer(serializers.ModelSerializer):
    
    companion = serializers.SerializerMethodField()
    def get_companion(self, instance):
        return instance.companion.title

    # writer = serializers.SerializerMethodField()
    # def get_writer(self, instance):
    #     return instance.writer.nickname

    class Meta:
        model = CoComment
        fields = ['id', 'writer', 'content', 'companion', 'like_count', 'created_at']
        read_only = ['id', 'writer', 'companion', 'like_count', 'created_at']