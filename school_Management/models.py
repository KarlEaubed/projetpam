from django.db import models
from utilisateurs.models import User_Main,CustomUserManager
from sitewebpam.models import*


class Site_School_Management(models.Model):
    title = models.CharField(max_length=200)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE)
    Couleur = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Modèle Classes
class Classes(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code_classe = models.CharField(max_length=100,unique=True)
    nom = models.CharField(max_length=100)
    effectif = models.IntegerField()
    program = models.TextField()
    
    
    
# Modèle Enseignants
class Enseignants(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    nom_cours = models.CharField(max_length=100)
    nombres_heures = models.IntegerField(null=True)
    groupe_sanguin = models.CharField(max_length=3)
    images = models.ImageField(upload_to='static/images/', null=True)
    pieces_identite_valide = models.DateField(null=True)
    date_de_rentree = models.DateField()

# Modèle Etudiants
class Etudiants(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code_etudiant = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    adresse = models.TextField()
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=3, null=True)
    date_entre = models.DateField()


# Modèle Cours
class Cours(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code_cours = models.CharField(max_length=100,unique=True)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    classe = models.CharField(max_length=100)
    nbre_heure = models.IntegerField()
    enseignant = models.ForeignKey(Enseignants, on_delete=models.CASCADE)
    


# Modèle Examens
class Examens(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code_examen = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    date = models.DateField()
    coefficient = models.IntegerField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)



# Modèle Programmes
class Programmes(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code_prog = models.CharField(max_length=100,unique=True)
    nom = models.CharField(max_length=100)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    description = models.TextField()
    cours = models.ManyToManyField(Cours)

# Modèle Petit Personnel
class PetitPersonnel(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code = models.CharField(max_length=100,unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    date_embauche = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=100)
    email = models.EmailField()

# Modèle Economat
class Economat(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code = models.CharField(max_length=100,unique=True)
    etudiants = models.ForeignKey(Etudiants, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    Montant = models.DecimalField(max_digits=10, decimal_places=2)
    versement1 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    versement2 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    versement3 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    versement4 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    versement5 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    versement_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)

# Modèle Fournitures
class Fournitures(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    code = models.CharField(max_length=100,unique=True)
    nom = models.CharField(max_length=100)
    types = models.CharField(max_length=100)
    date = models.DateField()
    etat = models.CharField(max_length=100)

# Modèle Horaires (à définir selon les besoins)
class Horaires(models.Model):
    site = models.ForeignKey(Site_School_Management, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours,on_delete=models.CASCADE)
    classe = models.ForeignKey(Classes,on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignants,on_delete=models.CASCADE)
    lundi = models.CharField(max_length=50,null=True)
    mardi = models.CharField(max_length=50,null=True)
    mercredi = models.CharField(max_length=50,null=True)
    jeudi = models.CharField(max_length=50,null=True)
    vendredi = models.CharField(max_length=50,null=True)
    samedi = models.CharField(max_length=50,null=True)


