# Generated by Django 5.0.7 on 2024-07-30 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='secret',
        ),
    ]
