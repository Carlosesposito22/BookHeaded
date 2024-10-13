# Generated by Django 5.1.1 on 2024-10-13 12:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_cc', '0003_profile_seguindo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clube',
            name='favoritado',
        ),
        migrations.AddField(
            model_name='clube',
            name='favoritos',
            field=models.ManyToManyField(blank=True, related_name='clubes_favoritos', to=settings.AUTH_USER_MODEL),
        ),
    ]
