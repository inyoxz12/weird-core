from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    friends_count = serializers.IntegerField(source='friends.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'display_name', 'first_name', 'last_name',
            'avatar', 'favorite_color', 'status_message', 'is_online', 'last_seen',
            'friends_count',
        ]
        read_only_fields = ['id', 'is_online', 'last_seen', 'friends_count']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'display_name', 'favorite_color']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    to_user_id = serializers.PrimaryKeyRelatedField(
        source='to_user',
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'to_user_id', 'status', 'created_at', 'responded_at']
        read_only_fields = ['id', 'status', 'created_at', 'responded_at', 'from_user', 'to_user']
