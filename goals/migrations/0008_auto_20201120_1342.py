# Generated by Django 3.1.2 on 2020-11-20 12:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0007_auto_20201120_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='users_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
