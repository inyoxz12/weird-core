from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet

router = DefaultRouter()
router.register('rooms', ChatRoomViewSet, basename='chatroom')

message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
message_detail = MessageViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})

urlpatterns = [
    path('', include(router.urls)),
    path('rooms/<int:room_pk>/messages/', message_list, name='message-list'),
    path('rooms/<int:room_pk>/messages/<int:pk>/', message_detail, name='message-detail'),
]
