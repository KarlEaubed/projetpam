from django.db import models
from sitewebpam.models import Sitewebpam
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password

class Site_Hospital_Management(models.Model):
    title = models.CharField(max_length=200)
    id_sitepam = models.ForeignKey(Sitewebpam, on_delete=models.CASCADE)
    Couleur = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='static/images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Medecin(models.Model):
    site = models.ForeignKey(Site_Hospital_Management, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=8)
    tel = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True)
    date_admission = models.DateField()
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Patient(models.Model):
    site = models.ForeignKey(Site_Hospital_Management, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=8)
    tel = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Consultation(models.Model):
    site = models.ForeignKey(Site_Hospital_Management, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    poids = models.FloatField()
    hauteur = models.IntegerField()
    diagnostique = models.TextField()
    date_consultation = models.DateField()

    def __str__(self):
        return f"Consultation de {self.patient} avec {self.medecin} le {self.date_consultation}"

class Prescription(models.Model):
    site = models.ForeignKey(Site_Hospital_Management, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    prescription = models.TextField()

    def __str__(self):
        return f"Prescription pour la consultation {self.consultation}"

class Dossier(models.Model):
    site = models.ForeignKey(Site_Hospital_Management, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    date_enregistrement = models.DateField()

    def __str__(self):
        return f"Dossier {self.code} enregistré le {self.date_enregistrement}"

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
    site = models.ForeignKey(Site_Hospital_Management, on_delete=models.CASCADE)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
