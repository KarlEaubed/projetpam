from django.db import models
from utilisateurs.models import *
from sitewebpam.models import*
# Create your models here.

class Admin_School(models.Model):
    email = models.CharField(max_length=100)
    password = models.TextField()
    grade = models.CharField(max_length=5)
    

    
    

    
class Site_School_Management(models.Model):
    title = models.CharField(max_length=200)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE)
    id_Admin_school = models.ForeignKey(Admin_School, on_delete=models.CASCADE)
    Couleur = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Classe_School(models.Model):
    nom_classe = models.CharField(max_length=50)
    niveau_etudes = models.CharField(max_length=50)

class Matiere_School(models.Model):
    nom_matiere = models.CharField(max_length=100)
    description = models.TextField()
    niveau_etudes = models.ForeignKey(Classe_School,on_delete=models.CASCADE) 

class Etudiant_School(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    niveau_etudes = models.CharField(max_length=50)
    classe = models.ForeignKey(Classe_School, on_delete=models.CASCADE)  

class Enseignant_School(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    matiere_enseignee = models.CharField(max_length=100)
    classe = models.ForeignKey(Classe_School, on_delete=models.CASCADE)  

class Note_School(models.Model):
    etudiant = models.ForeignKey(Etudiant_School, on_delete=models.CASCADE)  
    matiere = models.ForeignKey(Matiere_School, on_delete=models.CASCADE)  
    note = models.DecimalField(max_digits=5, decimal_places=2)

class Paiement_School(models.Model):
    etudiant = models.ForeignKey(Etudiant_School, on_delete=models.CASCADE)  
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()

class EmployeAdministratif_School(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    poste_occupe = models.CharField(max_length=100)

class Evenement_School(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_evenement = models.DateField()
    lieu = models.CharField(max_length=100)

class BulletinScolaire_School(models.Model):
    etudiant = models.ForeignKey(Etudiant_School, on_delete=models.CASCADE)  
    semestre = models.IntegerField()
    annee_scolaire = models.CharField(max_length=20)
    moyenne_generale = models.DecimalField(max_digits=5, decimal_places=2)
    remarques = models.TextField()

class Absence_School(models.Model):
    etudiant = models.ForeignKey(Etudiant_School, on_delete=models.CASCADE)  
    date_absence = models.DateField()
    motif_absence = models.CharField(max_length=100)

class Message_School(models.Model):
    site = models.ForeignKey(Site_School_Management,on_delete=models.CASCADE)
    object = models.CharField(null=True, max_length=50)
    content = models.CharField( max_length=255)
    Admin_School = models.ForeignKey(Admin_School,null=True, on_delete=models.CASCADE)
    Etudiant_School = models.ForeignKey(Etudiant_School, null=True, on_delete=models.CASCADE)
    Enseignant_School = models.ForeignKey(Enseignant_School, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    statut = models.CharField( max_length=50)
    
    
class Infos_School(models.Model):
    site = models.ForeignKey(Site_School_Management,on_delete=models.CASCADE)
    phone1 = models.CharField( max_length=50 )
    phone2 = models.CharField(null=True, max_length=50 )
    adresse = models.CharField(null=True, max_length=255 )
    about = models.CharField(null=True, max_length=255 )
    Bio = models.CharField(null=True, max_length=255 )
    Infos_supplementaires = models.CharField(null=True, max_length=255 )