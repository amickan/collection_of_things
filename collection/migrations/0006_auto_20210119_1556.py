# Generated by Django 2.2.9 on 2021-01-19 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_upload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='created',
        ),
        migrations.RemoveField(
            model_name='upload',
            name='updated',
        ),
    ]
