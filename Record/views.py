from .models import Record, RComment, Tag
from .serializers import RecordSerializer, RecordListSerializer, RCommentSerializer

from rest_framework import viewsets

class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    def get_serializer_class(self):
        if self.action == "list":
            return RecordListSerializer
        return RecordSerializer