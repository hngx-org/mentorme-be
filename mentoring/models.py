import uuid
from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Resource(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    price = models.FloatField()
    
    def __str__(self):
        return self.title

class Session(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField()
    no_of_sessions = models.IntegerField()
    relevant_topics = models.ForeignKey(Category, on_delete=models.CASCADE)
    occurence = models.IntegerField()
    
    def __str__(self):
        return self.name