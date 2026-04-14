from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    property = models.ForeignKey(
        'rentals.Property',
        on_delete=models.CASCADE,
        related_name='chat_rooms',
        blank=True,
        null=True
    )
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='renter_chat_rooms',
        blank=True,
        null=True
    )
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='landlord_chat_rooms',
        blank=True,
        null=True
    )
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"