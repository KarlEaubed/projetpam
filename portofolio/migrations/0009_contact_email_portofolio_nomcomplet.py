# Generated by Django 4.2.7 on 2024-05-13 15:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portofolio', '0008_contact_email_portofolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_email_portofolio',
            name='nomComplet',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
