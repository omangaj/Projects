# Generated by Django 5.0.6 on 2024-12-12 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_contact_info_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_info',
            name='fax',
            field=models.IntegerField(default='', null=True),
        ),
    ]
