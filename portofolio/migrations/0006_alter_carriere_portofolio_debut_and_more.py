# Generated by Django 4.2.7 on 2024-05-13 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portofolio', '0005_etude_portofolio_carriere_portofolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carriere_portofolio',
            name='debut',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='carriere_portofolio',
            name='fin',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='etude_portofolio',
            name='debut',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='etude_portofolio',
            name='fin',
            field=models.DateField(),
        ),
    ]
