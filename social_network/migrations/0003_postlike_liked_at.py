# Generated by Django 3.2.3 on 2021-05-22 11:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0002_auto_20210522_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlike',
            name='liked_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
