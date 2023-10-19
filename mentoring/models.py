import uuid
from django.db import models
from community.models import Community
from users.models import CustomUser

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
    link = models.URLField(null=True, blank=True)
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
    no_of_sessions = models.IntegerField(null=True)
    relevant_topics = models.ForeignKey(Category, on_delete=models.CASCADE)
    occurence = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    graduation_year = models.IntegerField(null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.degree


class Industry(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Certification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    issuer = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return self.name


class Identity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    gov_id_type = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255)
    id_link = models.URLField()  # Compulsory

    def __str__(self):
        return self.name


class Mentor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT)
    experience = models.IntegerField(default=0)
    skills = models.ForeignKey(Skill, on_delete=models.PROTECT)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    other_links = models.CharField(max_length=255, blank=True, null=True)
    mentoring_exp = models.IntegerField(default=0)
    mentoring_type = models.CharField(max_length=255, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)
    prefered_starttime = models.TimeField(blank=True, null=True)
    prefered_endtime = models.TimeField(blank=True, null=True)
    prefered_days = models.CharField(max_length=255, blank=True, null=True)
    education = models.ForeignKey(Education, on_delete=models.PROTECT)
    certification = models.ForeignKey(Certification, on_delete=models.PROTECT)
    identity = models.ForeignKey(Identity, on_delete=models.PROTECT)
    status = models.CharField(max_length=255, blank=True, null=True)
    resources = models.ForeignKey(Resource, on_delete=models.PROTECT)
    sessions = models.ForeignKey(Session, on_delete=models.PROTECT)

    def __str__(self):
        return self.user


class Mentee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    goals = models.CharField(max_length=255)

    def __str__(self):
        return self.title