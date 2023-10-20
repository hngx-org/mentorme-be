import uuid
from django.db import models
from community.models import Community
from users.models import CustomUser

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    link = models.URLField(null=True, blank=True)
    price = models.FloatField()

    def __str__(self):
        return self.title


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    graduation_year = models.IntegerField(null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.degree


class Industry(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    workplace = models.CharField(max_length=255)

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
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, null=True, blank=True)
    yearsofExp = models.IntegerField(default=0)
    skills = models.ForeignKey(Skill, on_delete=models.PROTECT, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    other_links = models.CharField(max_length=255, blank=True, null=True)
    mentoring_exp = models.IntegerField(default=0)
    mentoring_type = models.CharField(max_length=255, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)
    prefered_time = models.CharField(max_length=225, blank=True, null=True)
    prefered_days = models.CharField(max_length=255, blank=True, null=True)
    education = models.ForeignKey(Education, on_delete=models.PROTECT, null=True)
    certification = models.ForeignKey(Certification, on_delete=models.PROTECT, null=True)
    identity = models.ForeignKey(Identity, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    resources = models.ForeignKey(Resource, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Mentee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    goals = models.CharField(max_length=255)
    skills = models.ForeignKey(Skill, on_delete=models.PROTECT, null=True)
    experience = models.ForeignKey(Experience, on_delete=models.PROTECT, null=True)
    links = models.CharField(max_length=255, blank=True, null=True)
    preferred_mentor_country = models.CharField(max_length=255)
    tools = models.CharField(max_length=255, blank=True, null=True)
    discipline = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
         return self.user.email


class Session(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    start_time = models.TimeField()
    relevant_topics = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, null=True)
    # mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE, null=True)
    # free
    attendees_limit = models.IntegerField(null=True)
    
    # one-off
    session_type = models.CharField(max_length=100, null=True)
    
    # recurring
    occurence = models.IntegerField(null=True)
    no_of_sessions = models.IntegerField(null=True)
    status = models.CharField(max_length=100, null=True, default='Pending')
    def __str__(self):
        return self.name

class SessionBooking(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    session = models.ForeignKey(Session, on_delete=models.PROTECT, null=True)
    available_time_slot = models.TimeField()
    time_zone = models.CharField(max_length=100)
    subscription_plans = models.CharField(max_length=100)
    pricing = models.FloatField()
    notes = models.CharField(max_length=255)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE, null=True)
    

