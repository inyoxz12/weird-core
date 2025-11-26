from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionOfTheDayViewSet, QuestionAnswerViewSet, StoryViewSet

router = DefaultRouter()
router.register('questions', QuestionOfTheDayViewSet, basename='question')
router.register('stories', StoryViewSet, basename='story')

answer_list = QuestionAnswerViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
answer_detail = QuestionAnswerViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_pk>/answers/', answer_list, name='answer-list'),
    path('questions/<int:question_pk>/answers/<int:pk>/', answer_detail, name='answer-detail'),
]
