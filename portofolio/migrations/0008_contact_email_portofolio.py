# Generated by Django 4.2.7 on 2024-05-13 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portofolio', '0007_skill_portofolio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Email_Portofolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_proprio', models.EmailField(max_length=255, null=True)),
                ('email_visitor', models.EmailField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('budget', models.CharField(max_length=100, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portofolio.services_portofolio')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portofolio.site_portofolio')),
            ],
        ),
    ]
