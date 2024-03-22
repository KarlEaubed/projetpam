from django.db import models
from utilisateurs.models import *
from sitewebpam.models import*

# Create your models here.

# Create your models here.

class Site_Portofolio(models.Model):
    title = models.CharField(max_length=200)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE)
    Couleur = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Infos_Portofolio(models.Model):
    site=models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE )
    nom = models.TextField(max_length=50)
    prenom = models.TextField(max_length=50)
    phone = models.TextField(max_length=50)
    email = models.CharField(max_length=100)
    adresse = models.TextField(max_length=50)
    location = models.TextField(max_length=50)
    
class About_Portofolio(models.Model):
    site=models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE )
    texte = models.CharField(max_length=255)
    autre = models.TextField(null=True,max_length=255)
    
class Category_Portofolio(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Project_Portofolio(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category_Portofolio)
    created_at = models.DateTimeField(auto_now_add=True)
    links = models.TextField()


class Like_Portofolio(models.Model):
    post = models.ForeignKey(Project_Portofolio, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User_Standard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Follower_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio, on_delete=models.CASCADE)
    User_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Note_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio, on_delete=models.CASCADE)
    User_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    valeur = models.CharField( max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Partage_Portofolio(models.Model):
    data_post = models.ForeignKey(Project_Portofolio,null=True, on_delete=models.CASCADE)
    data_site = models.ForeignKey(Sitewebpam,null=True, on_delete=models.CASCADE)
    user_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Message_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE)
    object = models.ForeignKey(null=True, on_delete=models.CASCADE)
    content = models.ForeignKey( on_delete=models.CASCADE)
    user_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    statut = models.CharField( max_length=50)
    
    
class Services_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE)
    titre = models.CharField( max_length=50 )
    image = models.CharField(null=True, max_length=50 )
    descriptions = models.CharField(null=True, max_length=255 )
    autres = models.CharField(null=True, max_length=255 )

    
class Heroes_Portofolio(models.Model):
    site = models.ForeignKey(Site_Portofolio,on_delete=models.CASCADE)
    titre1 = models.CharField( max_length=50 )
    titre2 = models.CharField(null=True, max_length=50 )
    paragraphe = models.CharField(null=True, max_length=255 )
    cv = models.CharField(null=True, max_length=255 )
   