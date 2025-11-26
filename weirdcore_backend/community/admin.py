from django.contrib import admin
from .models import QuestionOfTheDay, QuestionAnswer, Story

@admin.register(QuestionOfTheDay)
class QuestionOfTheDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'is_active', 'created_at')
    list_filter = ('is_active',)

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'user', 'created_at')

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'created_at')
