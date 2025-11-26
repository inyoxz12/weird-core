from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class User(AbstractUser):
    display_name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    favorite_color = models.CharField(max_length=20, blank=True)
    status_message = models.CharField(max_length=140, blank=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='friends_with')

    def __str__(self):
        return self.username

class FriendRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_ACCEPTED, 'Aceptada'),
        (STATUS_REJECTED, 'Rechazada'),
    ]

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def accept(self):
        if self.status != self.STATUS_PENDING:
            return
        self.status = self.STATUS_ACCEPTED
        self.responded_at = timezone.now()
        self.save()
        self.from_user.friends.add(self.to_user)
        self.to_user.friends.add(self.from_user)

    def reject(self):
        if self.status != self.STATUS_PENDING:
            return
        self.status = self.STATUS_REJECTED
        self.responded_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"
