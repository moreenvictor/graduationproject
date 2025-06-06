# Generated by Django 5.2 on 2025-04-18 05:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_userprofile_user_type_userprofile_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recyclebag',
            name='order_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recyclebag',
            name='order_confirmed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('total_count', models.IntegerField()),
                ('material_type', models.CharField(max_length=100)),
                ('recycle_bag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.recyclebag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
