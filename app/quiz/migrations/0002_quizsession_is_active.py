# Generated by Django 5.1.4 on 2024-12-17 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizsession',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
