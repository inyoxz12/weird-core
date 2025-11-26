from django.contrib import admin
from .models import ChatRoom, Message, RandomQueue

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'room_type', 'created_by', 'created_at', 'is_active')
    list_filter = ('room_type', 'is_active')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'message_type', 'created_at')
    list_filter = ('message_type',)

@admin.register(RandomQueue)
class RandomQueueAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
