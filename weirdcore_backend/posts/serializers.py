from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Reaction
from users.serializers import UserSerializer

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

class ReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'post', 'user', 'type', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    reactions = ReactionSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    reactions_count = serializers.IntegerField(source='reactions.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'image', 'created_at', 'updated_at',
            'is_public', 'comments', 'reactions', 'comments_count', 'reactions_count',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'comments', 'reactions', 'comments_count', 'reactions_count']
