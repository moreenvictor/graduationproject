# Generated by Django 5.1.7 on 2025-03-20 00:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_recycleditem_weight_recycleditem_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recycleditem',
            name='count',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
