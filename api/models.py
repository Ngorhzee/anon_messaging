from django.db import models
from shared.abstractmodel import AbstractModel
from uuid import uuid4


class ChatRoom(AbstractModel):
    name = models.CharField(max_length=50, null=True)
    

class Messages(AbstractModel):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    content = models.CharField(max_length=500)
    device_id = models.UUIDField(default=uuid4)
