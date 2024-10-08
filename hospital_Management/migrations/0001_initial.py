# Generated by Django 4.2.7 on 2024-07-01 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sitewebpam', '0003_plan_alter_abonement_date_debut_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poids', models.FloatField()),
                ('hauteur', models.IntegerField()),
                ('diagnostique', models.TextField()),
                ('date_consultation', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Site_Hospital_Management',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('Couleur', models.CharField(max_length=50)),
                ('logo', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_sitepam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sitewebpam.sitewebpam')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription', models.TextField()),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.consultation')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.site_hospital_management')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('sexe', models.CharField(max_length=8)),
                ('tel', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=100)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.site_hospital_management')),
            ],
        ),
        migrations.CreateModel(
            name='Medecin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('sexe', models.CharField(max_length=8)),
                ('tel', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('specialite', models.CharField(max_length=50)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.site_hospital_management')),
            ],
        ),
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_enregistrement', models.DateField()),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.consultation')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.site_hospital_management')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='medecin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.medecin'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.patient'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_Management.site_hospital_management'),
        ),
    ]
