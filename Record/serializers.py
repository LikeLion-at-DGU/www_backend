from rest_framework import serializers
from .models import *



class RecordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Record
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'views']

    image = serializers.ImageField(use_url=True, required=False)


class RCommentSerializer(serializers.ModelSerializer):
    record = serializers.SerializerMethodField()

    def get_record(self, instance):
        return instance.record.title

    class Meta:
        model = RComment
        fields = '__all__'
        read_only_fields = ['record']

class RecordListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    class Meta:
        model = Record
        fields = [
            "id",
            "created_at",
            "updated_at",
            "comments_cnt",
            "title",
            "weather",
            "body",
            "writer",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "comments_cnt"]