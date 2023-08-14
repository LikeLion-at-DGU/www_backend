from rest_framework import serializers
from .models import *



class RecordSerializer(serializers.ModelSerializer):
    # Record 댓글 가져오기
    record_comments = serializers.SerializerMethodField(read_only=True)
    # Record 카드 가져오기
    record_cards = serializers.SerializerMethodField(read_only=True)

    # Record 모델에 댓글이 없으니깐....댓글도 가져오기
    def get_record_comments(self, instance):
        serializer = RCommentSerializer(instance.rcomments, many=True)
        return serializer.data
    
    # Record 모델에 카드가 없으니깐....카드도 가져오기
    def get_record_cards(self, instance):
        serializer = CardSerializer(instance.cards, many=True)
        return serializer.data

    class Meta:
        model = Record
        fields = "__all__"
        # 작성 안해주고 읽기만 해주는 필드
        read_only_fields = ['id', 'created_at', 'updated_at', 'views', 'likes',]

    image = serializers.ImageField(use_url=True, required=False)


class RCommentSerializer(serializers.ModelSerializer):
    record = serializers.SerializerMethodField()

    def get_record(self, instance):
        return instance.record.title

    class Meta:
        model = RComment
        fields = '__all__'
        read_only_fields = ['record']


# Record List
class RecordListSerializer(serializers.ModelSerializer):
    rcomments_cnt = serializers.SerializerMethodField()

    def get_rcomments_cnt(self, instance):
        return instance.rcomments.count()
    
    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ["id", "created_at", "updated_at", "rcomments_cnt"]


# Card 시리얼라이저
class CardSerializer(serializers.ModelSerializer):
    record = serializers.SerializerMethodField()

    def get_record(self, instance):
        return instance.record.title

    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ['record']


# Upload_image 시리얼라이저
class Upload_imageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Upload_image
        fields = '__all__'