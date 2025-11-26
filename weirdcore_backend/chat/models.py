from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    PRIVATE = 'private'
    GROUP = 'group'
    RANDOM = 'random'

    ROOM_TYPE_CHOICES = [
        (PRIVATE, 'Privado'),
        (GROUP, 'Grupo'),
        (RANDOM, 'Random'),
    ]

    name = models.CharField(max_length=255)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default=GROUP)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_chat_rooms', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.room_type})"

class Message(models.Model):
    TEXT = 'text'
    EMOJI = 'emoji'
    BUZZ = 'buzz'
    IMAGE = 'image'
    AUDIO = 'audio'
    DRAWING = 'drawing'
    SYSTEM = 'system'

    MESSAGE_TYPE_CHOICES = [
        (TEXT, 'Texto'),
        (EMOJI, 'Emoji'),
        (BUZZ, 'Zumbido'),
        (IMAGE, 'Imagen'),
        (AUDIO, 'Audio'),
        (DRAWING, 'Dibujo'),
        (SYSTEM, 'Sistema'),
    ]

    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default=TEXT)
    content = models.TextField(blank=True)
    # Para imágenes, audios, dibujos o datos extra, el frontend puede enviar JSON aquí.
    extra_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Mensaje {self.id} en {self.room_id} por {self.sender_id}"

class RandomQueue(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='random_queue_entry', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RandomQueue({self.user})"
