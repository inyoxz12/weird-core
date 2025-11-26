from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import QuestionOfTheDay, QuestionAnswer, Story
from users.serializers import UserSerializer

User = get_user_model()

class QuestionOfTheDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOfTheDay
        fields = ['id', 'question', 'is_active', 'created_at']

class QuestionAnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = QuestionAnswer
        fields = ['id', 'question', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class StorySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'author', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
