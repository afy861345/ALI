# Generated by Django 5.1.5 on 2025-01-16 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_topic_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
