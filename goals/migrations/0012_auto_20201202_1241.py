# Generated by Django 3.1.3 on 2020-12-02 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0011_auto_20201202_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
