from django.db import models
from utilisateurs.models import *

# Create your models here.

class Abonement(models.Model):
    id_user = models.ForeignKey(User_Main, on_delete=models.CASCADE)
    type_abonnement = models.CharField(max_length = 50)     
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField()
   
    
    
class Sitewebpam(models.Model):
    id_user = models.ForeignKey(User_Main, on_delete=models.CASCADE)
    id_abonnement= models.ForeignKey(Abonement, on_delete=models.CASCADE, null=True)
    domaine = models.CharField(max_length = 100)
    nom_site = models.CharField(max_length = 150, null=True)
    type = models.CharField(max_length = 50)
    stockage = models.CharField(max_length = 150, null=True)
    terms_conditions = models.BooleanField(default=False)
 
class Info_utilisateurs(models.Model):
    id_user = models.ForeignKey(User_Main, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)