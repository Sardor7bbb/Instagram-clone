from django.urls import path

from stories.views import StoryCreateAPIView, StoryViewCreateAPIView, UserStoryListAPIView, StoryViewListAPIView, \
    StoryReactionCreateAPIView, StoryReportCreateAPIView

app_name = 'stories'

urlpatterns = [
    path('upload/', StoryCreateAPIView.as_view(), name='upload'),
    path('view/', StoryViewCreateAPIView.as_view(), name='view-create'),
    path('view/<int:story_id>/', StoryViewListAPIView.as_view(), name='views'),
    path('user/', UserStoryListAPIView.as_view(), name='user'),
    path('react/', StoryReactionCreateAPIView.as_view(), name='react'),
    path('report/', StoryReportCreateAPIView.as_view(), name='report'),
]



