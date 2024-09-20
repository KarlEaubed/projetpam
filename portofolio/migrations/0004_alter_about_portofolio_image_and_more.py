# Generated by Django 5.0.3 on 2024-05-09 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portofolio', '0003_alter_site_portofolio_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about_portofolio',
            name='image',
            field=models.ImageField(null=True, upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='heroes_portofolio',
            name='image',
            field=models.ImageField(null=True, upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='pro_portofolio',
            name='image',
            field=models.ImageField(null=True, upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='services_portofolio',
            name='image',
            field=models.ImageField(null=True, upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='site_portofolio',
            name='logo',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
