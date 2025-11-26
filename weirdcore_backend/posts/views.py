from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Post, Comment, Reaction
from .serializers import PostSerializer, CommentSerializer, ReactionSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = user.friends.all()
        return Post.objects.filter(
            Q(author=user) | Q(author__in=friends),
            is_public=True
        ).select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs.get('post_pk'))

class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reaction.objects.filter(post_id=self.kwargs.get('post_pk'))

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_pk')
        type_ = request.data.get('type', Reaction.LIKE)
        reaction, created = Reaction.objects.get_or_create(
            post_id=post_id,
            user=request.user,
            defaults={'type': type_},
        )
        if not created:
            if reaction.type == type_:
                reaction.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            reaction.type = type_
            reaction.save()
        serializer = self.get_serializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
