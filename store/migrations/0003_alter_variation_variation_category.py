# Generated by Django 4.2.2 on 2023-06-19 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'couleur'), ('size', 'taille')], max_length=128),
        ),
    ]
