from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChatRoom, Message, RandomQueue
from .serializers import ChatRoomSerializer, MessageSerializer

User = get_user_model()

class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(participants=user, is_active=True).prefetch_related('participants')

    def perform_create(self, serializer):
        room = serializer.save(created_by=self.request.user)
        room.participants.add(self.request.user)

    @action(detail=False, methods=['post'])
    def private_room(self, request):
        other_user_id = request.data.get('other_user_id')
        if not other_user_id:
            return Response({'detail': 'other_user_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        qs = ChatRoom.objects.filter(
            room_type=ChatRoom.PRIVATE,
            participants=user
        ).filter(participants=other_user)
        room = qs.first()
        if not room:
            room = ChatRoom.objects.create(
                name=f"Chat {user.username} & {other_user.username}",
                room_type=ChatRoom.PRIVATE,
                created_by=user,
            )
            room.participants.set([user, other_user])
        serializer = self.get_serializer(room)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def random_room(self, request):
        user = request.user
        with transaction.atomic():
            try:
                entry = RandomQueue.objects.select_for_update().exclude(user=user).earliest('created_at')
            except RandomQueue.DoesNotExist:
                RandomQueue.objects.update_or_create(user=user, defaults={})
                return Response({'detail': 'Esperando otro usuario para random chat'}, status=status.HTTP_202_ACCEPTED)

            other_user = entry.user
            entry.delete()

            room = ChatRoom.objects.create(
                name='Random Chat',
                room_type=ChatRoom.RANDOM,
                created_by=user,
            )
            room.participants.set([user, other_user])

        serializer = self.get_serializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        room_id = self.kwargs.get('room_pk')
        qs = Message.objects.filter(room_id=room_id, room__participants=user)
        return qs

    def perform_create(self, serializer):
        room_id = self.kwargs.get('room_pk')
        room = ChatRoom.objects.filter(id=room_id, participants=self.request.user).first()
        if not room:
            raise PermissionError('No participas en esta sala')
        serializer.save(sender=self.request.user, room=room)
