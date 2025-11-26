from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import FriendRequest
from .serializers import UserSerializer, RegisterSerializer, FriendRequestSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['display_name'] = user.display_name or user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(username__icontains=search)
        return qs

    @action(detail=False, methods=['get'])
    def online(self, request):
        users = self.get_queryset().filter(is_online=True)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user) | FriendRequest.objects.filter(from_user=user)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        fr = self.get_object()
        if fr.to_user != request.user:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        fr.accept()
        return Response(self.get_serializer(fr).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        fr = self.get_object()
        if fr.to_user != request.user:
            return Response({'detail': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        fr.reject()
        return Response(self.get_serializer(fr).data)
