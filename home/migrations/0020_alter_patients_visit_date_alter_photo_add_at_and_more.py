# Generated by Django 5.1.5 on 2025-01-19 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_photo_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='visit_date',
            field=models.DateField(default='2025-01-19', null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='add_at',
            field=models.DateField(default='2025-01-19'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateField(default='2025-01-19'),
        ),
    ]