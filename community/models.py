from django.db import models
from users.models import *
import uuid



class Community(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    discussions = models.ManyToManyField('Discussion')


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)


class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    comments = models.ForeignKey(Comment, on_delete=models.PROTECT)
    image = models.URLField(null=True, blank=True)




