from rest_framework import serializers
from .models import Profile


# Profile 시리얼라이저
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"