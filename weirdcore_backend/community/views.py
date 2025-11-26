from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import QuestionOfTheDay, QuestionAnswer, Story
from .serializers import QuestionOfTheDaySerializer, QuestionAnswerSerializer, StorySerializer

class QuestionOfTheDayViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionOfTheDaySerializer
    queryset = QuestionOfTheDay.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'active']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def active(self, request):
        question = QuestionOfTheDay.objects.filter(is_active=True).order_by('-created_at').first()
        if not question:
            return Response({'detail': 'No hay pregunta activa'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(question)
        return Response(serializer.data)

class QuestionAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qid = self.kwargs.get('question_pk')
        return QuestionAnswer.objects.filter(question_id=qid)

    def perform_create(self, serializer):
        qid = self.kwargs.get('question_pk')
        serializer.save(user=self.request.user, question_id=qid)

class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    queryset = Story.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
