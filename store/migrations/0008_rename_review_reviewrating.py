# Generated by Django 4.2.2 on 2023-07-20 08:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0007_review'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Review',
            new_name='ReviewRating',
        ),
    ]