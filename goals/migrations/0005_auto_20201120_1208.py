# Generated by Django 3.1.2 on 2020-11-20 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0004_auto_20201120_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='status',
            field=models.CharField(choices=[('NS', 'Not started'), ('IP', 'In Progress'), ('AC', 'Accomplished')], default='In Progress', max_length=50),
        ),
    ]
