# Generated by Django 5.0.6 on 2024-10-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_level_course_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=100),
        ),
    ]
