from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Discussion, Choice, Comment
from .serializers import DiscussionSerializer

# Create your views here.
class DiscussionViewSet(viewsets.ModelViewSet):
    serializer_class = DiscussionSerializer
