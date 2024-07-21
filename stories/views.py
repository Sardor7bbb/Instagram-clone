from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from shared.custom_pagination import CustomPagination
from stories.models import StoryViewModel, StoryModel, StoryReactionModel, StoryReportModel
from stories.serializers import StorySerializer, StoryViewSerializer, StoryReactionSerializer, StoryReportSerializer


class StoryCreateAPIView(generics.CreateAPIView):
    queryset = StoryModel.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, expire_time=timezone.now() + timedelta(days=1), is_active=True)


class StoryViewCreateAPIView(generics.CreateAPIView):
    queryset = StoryViewModel.objects.all()
    serializer_class = StoryViewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        story_id = self.request.data['story']
        serializer.save(user=self.request.user, story_id=story_id)


class UserStoryListAPIView(generics.CreateAPIView):
    queryset = StoryModel.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return StoryModel.objects.filter(user=self.request.user, expire_time__gt=timezone.now())


class StoryViewListAPIView(generics.CreateAPIView):
    queryset = StoryViewModel.objects.all()
    serializer_class = StoryViewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return StoryViewModel.objects.filter(story_id=self.kwargs['story_id'])


class StoryReactionCreateAPIView(generics.CreateAPIView):
    queryset = StoryReactionModel.objects.all()
    serializer_class = StoryReactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        story_id = self.request.data['story']
        reaction = self.request.data['reaction']
        serializer.save(user=self.request.user, story_id=story_id, reaction=reaction)


class StoryReportCreateAPIView(generics.CreateAPIView):
    queryset = StoryReportModel.objects.all()
    serializer_class = StoryReportSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        story_id = self.request.data['story']
        reason = self.request.data['reason']
        serializer.save(user=self.request.user, story_id=story_id, reason=reason)
