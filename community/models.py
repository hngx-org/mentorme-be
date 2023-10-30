from django.db import models
from users.models import *
import uuid


class Community(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
class Members(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='member', on_delete=models.PROTECT)


class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    topic = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    creator = models.ForeignKey(CustomUser, related_name='author', on_delete=models.PROTECT)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(CustomUser, related_name='user_comment', on_delete=models.PROTECT)
    discusion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    text = models.TextField()






