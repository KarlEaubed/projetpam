from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User_Main

class UserMainAdmin(UserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('email', 'username', 'nom', 'prenom', 'portable', 'date_de_nais', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    
    # Champs pour la recherche
    search_fields = ('email', 'username', 'nom', 'prenom', 'portable')
    
    # Filtres latéraux
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'grade')
    
    # Champs pour la création et la modification d'un utilisateur dans l'admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'username', 'portable', 'date_de_nais', 'grade')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates importantes', {'fields': ('date_joined',)}),
        ('Autres', {'fields': ('created_by',)}),
    )

    # Champs obligatoires lors de la création d'un utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'username', 'portable', 'date_de_nais', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'grade'),
        }),
    )

    # Configuration du comportement par défaut
    ordering = ('email',)
    filter_horizontal = ()

# Enregistrer le modèle dans l'admin
admin.site.register(User_Main, UserMainAdmin)
