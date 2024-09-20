# Model Blog
from django.db import models
from utilisateurs.models import *
from sitewebpam.models import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password


# Create your models here.

    

class Category_Blog(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    
class Tag_Blog(models.Model):
    name = models.CharField(max_length=50)
    
class Site_Blog(models.Model):
    title = models.CharField(max_length=200)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE)
    id_Admin_Blog = models.ForeignKey(User_Main, on_delete=models.CASCADE)
    Couleur = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='static/images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category_Blog, related_name='site_blogs')
    tags = models.ManyToManyField(Tag_Blog, related_name='site_blogs')




class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(email, password, **extra_fields)

class User_Standard(AbstractBaseUser):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    initials = models.CharField(max_length=2)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    site = models.ForeignKey(Site_Blog, on_delete=models.CASCADE)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def check_password(self, raw_password):
        # Vérifie si le mot de passe brut correspond au mot de passe haché de l'utilisateur
        return check_password(raw_password, self.password)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    # Ajoutez d'autres méthodes personnalisées au besoin



class Post_Blog(models.Model):
    site = models.ForeignKey(Site_Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/images/', blank=True)
    content = models.TextField()
    author = models.ForeignKey(User_Main, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False) 
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


class Notification(models.Model):
    site = models.ForeignKey(Site_Blog, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User_Standard, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

    def __str__(self):
        return self.message


class SiteChoice(models.Model):
    site = models.ForeignKey(Site_Blog, on_delete=models.CASCADE)
    navbar_bg = models.CharField(max_length=50, default='color')
    navbar_font = models.CharField(max_length=50)
    navbar_font_size = models.CharField(max_length=50)
    navbar_brand = models.CharField(max_length=50, null=True)
    navbar_brand_color = models.CharField(max_length=50, null=True)
    navbar_link_color = models.CharField(max_length=50, null=True)
    navbar_link_1 = models.CharField(max_length=50, null=True)
    navbar_link_2 = models.CharField(max_length=50, null=True)
    navbar_link_3 = models.CharField(max_length=50, null=True)
    navbar_link_4 = models.CharField(max_length=50, null=True)
    navbar_link_size = models.CharField(max_length=50, null=True)