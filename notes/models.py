import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Note(models.Model):
    uuid = models.UUIDField(unique=True, null=False, blank=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False, default=uuid)
    content = models.TextField(null=False, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
