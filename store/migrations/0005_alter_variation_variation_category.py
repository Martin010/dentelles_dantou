# Generated by Django 4.2.2 on 2023-06-19 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('couleur', 'color'), ('taille', 'size')], max_length=128),
        ),
    ]