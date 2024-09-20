# Generated by Django 4.2.7 on 2024-06-04 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitewebpam', '0002_info_utilisateurs_image_info_utilisateurs_initials'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='abonement',
            name='date_debut',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='abonement',
            name='type_abonnement',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='abonement',
            name='plan',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sitewebpam.plan'),
            preserve_default=False,
        ),
    ]
