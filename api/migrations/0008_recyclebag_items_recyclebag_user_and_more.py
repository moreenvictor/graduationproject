# Generated by Django 5.1.7 on 2025-03-20 02:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_recyclebag_description_remove_recyclebag_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recyclebag',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='recyclebags', to='api.scanneditem'),
        ),
        migrations.AddField(
            model_name='recyclebag',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scanneditem',
            name='material_type',
            field=models.CharField(choices=[('plastic', 'Plastic'), ('can', 'Can'), ('glass', 'Glass')], default='plastic', max_length=10),
        ),
    ]
