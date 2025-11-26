from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'participants', 'created_by', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_by', 'is_active', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'sender_username', 'message_type', 'content', 'extra_data', 'created_at']
        read_only_fields = ['id', 'sender', 'sender_username', 'created_at']
