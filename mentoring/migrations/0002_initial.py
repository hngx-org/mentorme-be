# Generated by Django 4.2.6 on 2023-10-22 19:35

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
            model_name='resource',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mentor',
            name='certification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.certification'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.company'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='education',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.education'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='identity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.identity'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.industry'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='resources',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.resource'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='skills',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.skill'),
        ),
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
            name='experience',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.experience'),
        ),
        migrations.AddField(
            model_name='mentee',
            name='skills',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='mentoring.skill'),
        ),
        migrations.AddField(
            model_name='mentee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discussion',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentoring.community'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='discusion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentoring.discussion'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
