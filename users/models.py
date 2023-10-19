from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .managers import CustomUserManager
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractUser):
    """object model for the user entity"""
    username = None
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    image = models.URLField(max_length=1000)
    gender = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    bio = models.TextField()
    password = models.CharField(max_length=255, blank=False)
    email_verified = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    role = models.CharField(max_length=225, default='null')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Tokens(models.Model):
    email = models.EmailField('email address')
    action = models.CharField(max_length=20)
    token = models.CharField(max_length=200)
    exp_date = models.FloatField()
    date_used = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    used = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Hash the token before saving in the DB
        self.token = make_password(str(self.token))
        super().save(*args, **kwargs)