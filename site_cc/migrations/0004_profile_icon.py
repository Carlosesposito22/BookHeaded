# Generated by Django 5.1 on 2024-10-13 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_cc', '0003_profile_seguindo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='icon',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
