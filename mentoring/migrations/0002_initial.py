# Generated by Django 4.2 on 2023-10-19 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mentoring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mentee',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mentoring.company'),
        ),
        migrations.AddField(
            model_name='mentee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]