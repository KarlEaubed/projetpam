# Generated by Django 4.2.7 on 2024-06-04 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sitewebpam', '0003_plan_alter_abonement_date_debut_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_classe', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('effectif', models.IntegerField()),
                ('program', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_cours', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('classe', models.CharField(max_length=100)),
                ('nbre_heure', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Enseignants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=100)),
                ('nom_cours', models.CharField(max_length=100)),
                ('nombres_heures', models.IntegerField()),
                ('groupe_sanguin', models.CharField(max_length=3)),
                ('images', models.ImageField(null=True, upload_to='static/images/')),
                ('pieces_identite_valide', models.DateField(null=True)),
                ('date_de_rentree', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Site_School_Management',
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
            name='Programmes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_prog', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.classes')),
                ('cours', models.ManyToManyField(to='school_Management.cours')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management')),
            ],
        ),
        migrations.CreateModel(
            name='PetitPersonnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('poste', models.CharField(max_length=100)),
                ('salaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_embauche', models.DateField()),
                ('adresse', models.TextField()),
                ('telephone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management')),
            ],
        ),
        migrations.CreateModel(
            name='Horaires',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lundi', models.CharField(max_length=50, null=True)),
                ('mardi', models.CharField(max_length=50, null=True)),
                ('mercredi', models.CharField(max_length=50, null=True)),
                ('jeudi', models.CharField(max_length=50, null=True)),
                ('vendredi', models.CharField(max_length=50, null=True)),
                ('samedi', models.CharField(max_length=50, null=True)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.classes')),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.cours')),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.enseignants')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management')),
            ],
        ),
        migrations.CreateModel(
            name='Fournitures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('types', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('etat', models.CharField(max_length=100)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management')),
            ],
        ),
        migrations.CreateModel(
            name='Examens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_examen', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('coefficient', models.IntegerField()),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.classes')),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.cours')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management')),
            ],
        ),
        migrations.CreateModel(
            name='Etudiants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_etudiant', models.CharField(max_length=100, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=100)),
                ('adresse', models.TextField()),
                ('groupe_sanguin', models.CharField(max_length=3, null=True)),
                ('date_entre', models.DateField()),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.classes')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management')),
            ],
        ),
        migrations.AddField(
            model_name='enseignants',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management'),
        ),
        migrations.CreateModel(
            name='Economat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('Montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('versement1', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('versement2', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('versement3', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('versement4', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('versement5', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('versement_total', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.classes')),
                ('etudiants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.etudiants')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management')),
            ],
        ),
        migrations.AddField(
            model_name='cours',
            name='enseignant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.enseignants'),
        ),
        migrations.AddField(
            model_name='cours',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management'),
        ),
        migrations.AddField(
            model_name='classes',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_Management.site_school_management'),
        ),
    ]
