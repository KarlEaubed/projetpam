# Generated by Django 4.2.7 on 2024-06-03 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portofolio', '0011_design_site_portofolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design_site_portofolio',
            name='contact_choice',
            field=models.CharField(default='contact1.html', max_length=255),
        ),
        migrations.AlterField(
            model_name='design_site_portofolio',
            name='footer_choice',
            field=models.CharField(default='footer1.html', max_length=255),
        ),
        migrations.AlterField(
            model_name='design_site_portofolio',
            name='header_choice',
            field=models.CharField(default='header1.html', max_length=255),
        ),
        migrations.AlterField(
            model_name='design_site_portofolio',
            name='navbar_choice',
            field=models.CharField(default='navbar1.html', max_length=255),
        ),
        migrations.AlterField(
            model_name='design_site_portofolio',
            name='service_choice',
            field=models.CharField(default='service1.html', max_length=255),
        ),
    ]
