from django.db import models
from utilisateurs.models import *
from sitewebpam.models import*


# Create your models here.
class Admin_Blog(models.Model):
    email = models.CharField(max_length=100)
    password = models.TextField()
    grade = models.CharField(max_length=5)
    
class Category_Blog(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    
class Tag_Blog(models.Model):
    name = models.CharField(max_length=50)
    
class Site_Blog(models.Model):
    title = models.CharField(max_length=200)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE)
    id_Admin_Blog = models.ForeignKey(Admin_Blog, on_delete=models.CASCADE)
    Couleur = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Post_Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', blank=True)
    content = models.TextField()
    author = models.ForeignKey(Admin_Blog, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category_Blog)
    tags = models.ManyToManyField(Tag_Blog)
    slug = models.SlugField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment_Blog(models.Model):
    post = models.ForeignKey(Post_Blog, on_delete=models.CASCADE)
    
    author = models.ForeignKey(User_Standard, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like_Blog(models.Model):
    post = models.ForeignKey(Post_Blog, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment_Blog, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User_Standard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Follower_Blog(models.Model):
    site = models.ForeignKey(Site_Blog, on_delete=models.CASCADE)
    user_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Note_Blog(models.Model):
    site = models.ForeignKey(Site_Blog, on_delete=models.CASCADE)
    user_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    valeur = models.CharField( max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Partage_Blog(models.Model):
    data_post = models.ForeignKey(Post_Blog,null=True, on_delete=models.CASCADE)
    data_site = models.ForeignKey(Sitewebpam,null=True, on_delete=models.CASCADE)
    user_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
    user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
    user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
# class Message_Blog(models.Model):
#     site = models.ForeignKey(Site_Blog,on_delete=models.CASCADE)
#     object = models.ForeignKey(Post_Blog,null=True, on_delete=models.CASCADE)
#     content = models.ForeignKey(Sitewebpam,null=True, on_delete=models.CASCADE)
#     user_Standard = models.ForeignKey(User_Standard,null=True, on_delete=models.CASCADE)
#     user_livreur = models.ForeignKey(User_Livreur, null=True, on_delete=models.CASCADE)
#     user_main = models.ForeignKey(User_Main, null=True, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     statut = models.CharField( max_length=50)
    
    
class Infos_Blog(models.Model):
    site = models.ForeignKey(Site_Blog,on_delete=models.CASCADE)
    phone1 = models.CharField(null=True, max_length=50 )
    phone2 = models.CharField(null=True, max_length=50 )
    adresse = models.CharField(null=True, max_length=255 )
    about = models.CharField(null=True, max_length=255 )
    Bio = models.CharField(null=True, max_length=255 )
    Infos_supplementaires = models.CharField(null=True, max_length=255 )
