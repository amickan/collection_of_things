# Generated by Django 2.2.9 on 2021-01-20 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0006_auto_20210120_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
