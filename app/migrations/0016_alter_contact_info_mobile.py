# Generated by Django 5.0.6 on 2024-12-12 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_contact_info_fax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_info',
            name='mobile',
            field=models.IntegerField(),
        ),
    ]
