from rest_framework import serializers
from .models import *



class RecordSerializer(serializers.ModelSerializer):
    # Record 댓글 가져오기
    record_comments = serializers.SerializerMethodField(read_only=True)
    tag = serializers.SerializerMethodField()


    # Record 모델에 댓글이 없으니깐....댓글도 가져오기
    def get_record_comments(self, instance):
        serializer = RCommentSerializer(instance.rcomments, many=True)
        return serializer.data

    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Record
        fields = "__all__"
        # 작성 안해주고 읽기만 해주는 필드
        read_only_fields = ['id', 'created_at', 'updated_at', 'views', 'rlike', 'rlike_count', 'record_scrap', 'tag', 'card_scrap']
    
    card_photo_1 = serializers.ImageField(use_url=True, required=True) # 첫 사진은 required=True (사진 하나라도 있어야 업로드 가능)
    card_photo_2 = serializers.ImageField(use_url=True, required=False)
    card_photo_3 = serializers.ImageField(use_url=True, required=False)


# Card 시리얼라이저
class CardSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()

    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Record
        fields = ['where', 'what', 'how', 'tag_field', 'tag', 'card_photo_1', 'card_photo_2', 'card_photo_3', 'card_scrap', 'id', 'created_at']
        # 작성 안해주고 읽기만 해주는 필드
        read_only_fields = []



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
    tag = serializers.SerializerMethodField()

    def get_rcomments_cnt(self, instance):
        return instance.rcomments.count()
    

    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ["id", "created_at", "updated_at", "rcomments_cnt"]





# Upload_image 시리얼라이저
class Upload_imageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Upload_image
        fields = '__all__'