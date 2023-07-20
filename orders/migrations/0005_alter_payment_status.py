# Generated by Django 4.2.2 on 2023-07-19 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_orderproduct_variation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('CANCELED', 'Annulé'), ('CREATED', 'Créé'), ('COMPLETED', 'Complété'), ('INCOMPLETE', 'Incomplet'), ('ERROR', 'Erreur'), ('REVERSALERROR', "Erreur d'annulation"), ('PROCESSING', 'En cours'), ('PENDING', 'En attente')], default='CREATED', max_length=16),
        ),
    ]
