# Generated by Django 4.2.7 on 2024-09-21 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0002_remove_user_main_is_staff_user_main_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_main',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
