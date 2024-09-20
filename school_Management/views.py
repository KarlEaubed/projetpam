from django.http import HttpResponse
from django.shortcuts import redirect, render
from school_Management.models import *
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password




def create_site_school(request, site_id):

    if request.method == "POST":
        title = request.POST.get('title')
        couleur = request.POST.get('couleur')
        logo = request.FILES.get('logo')

        # Récupérer les instances de Sitewebpam et Admin_Blog correspondantes
        sitewebpam = Sitewebpam.objects.get(id=site_id)
        user = request.user

        # Créer une instance de Site_Blog avec les données du formulaire
        site_school = Site_School_Management.objects.create(
            title=title,
            id_sitepam=sitewebpam,
            Couleur=couleur,
            logo=logo
        )
        site_school.save()


        # Rediriger vers une nouvelle URL avec les paramètres appropriés
        return redirect('dashboard_school', domaine=sitewebpam.domaine) # Assurez-vous d'avoir la bonne URL ici

    # Dans votre vue Django
    return render(request, 'createsite.html', {'site_id': site_id})


def dashboard_school(request, domaine):
    user = request.user
    site = Sitewebpam.objects.filter(id_user=user).first()
    if site:
        site_school_info = Site_School_Management.objects.filter(id_sitepam=site).first()
        context = {
            'domaine' : domaine,
            'site_id' : site_school_info.id,
        }
        return render(request, 'school.html', context)
    else:
        return HttpResponse("No site found for the user.")

def logOut(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('home')

def create_enseignant(request, domaine, site_id):
    user = request.user # utilisateur connecte
    site = Sitewebpam.objects.filter(id_user=user).first()

    # Vérifier si un site a été trouvé pour l'utilisateur
    if site:
        site_school_info = Site_School_Management.objects.filter(id_sitepam=site).first()
        context = {
            'domaine' : site.domaine,
            'site_id' : site_school_info.id,
        }
        return render(request, 'create_enseignant.html', context)
    else:
        return HttpResponse("No site found for the user.")
    
    
    
    
        
def create_enseignant_logic(request, domaine, site_id):
    user = request.user # utilisateur connecte
    # Récupérer les informations du site lié à l'utilisateur connecté
    sitewebpam = Sitewebpam.objects.filter(id_user=user).first() 
    
    if request.method == "POST":
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('phone')
        adresse = request.POST.get('adresse')
        password = request.POST.get('password')
        nom_cours = request.POST.get('nom_cours')
        date_de_rentree = request.POST.get('date_de_rentree')
        
        try:
            site = Site_School_Management.objects.get(id=site_id)
        except Site_School_Management.DoesNotExist:
            messages.error(request, 'Site not found.')
            return render(request, 'create_enseignant.html', {'domaine': domaine, 'site_id': site_id})

        create_enseignant = Enseignants.objects.create(
            code=code,
            nom=nom,
            prenom=prenom,
            email=email,
            adresse=adresse,
            password=make_password(password),
            telephone=telephone,
            nom_cours=nom_cours,
            date_de_rentree=date_de_rentree,
            site_id=site_id,
        )
        create_enseignant.save()
        return redirect('dashboard_school', domaine=sitewebpam.domaine)
    return render(request, 'create_enseignant.html', {'domaine': domaine, 'site_id': site_id})





def create_examen_logic(request, domaine, site_id):
    user = request.user  # utilisateur connecté

    # Récupérer les informations du site lié à l'utilisateur connecté
    sitewebpam = Sitewebpam.objects.filter(id_user=user).first() 
    
    if request.method == "POST":
        code_examen = request.POST.get('code_examen')
        nom = request.POST.get('nom')
        classe_id = request.POST.get('classe')
        date = request.POST.get('date')
        coefficient = request.POST.get('coefficient')
        cours_id = request.POST.get('cours')
        
        try:
            site = Site_School_Management.objects.get(id=site_id)
        except Site_School_Management.DoesNotExist:
            messages.error(request, 'Site not found.')
            return render(request, 'create_examen.html', {'domaine': domaine, 'site_id': site_id})

        try:
            classe = Classes.objects.get(id=classe_id)
            cours = Cours.objects.get(id=cours_id)
        except (Classes.DoesNotExist, Cours.DoesNotExist):
            messages.error(request, 'Class or Course not found.')
            return render(request, 'create_examen.html', {'domaine': domaine, 'site_id': site_id})

        create_examen = Examens.objects.create(
            site=site,
            code_examen=code_examen,
            nom=nom,
            classe=classe,
            date=date,
            coefficient=coefficient,
            cours=cours,
        )
        create_examen.save()
        return redirect('dashboard_school', domaine=sitewebpam.domaine)
    
    classes = Classes.objects.all()
    cours = Cours.objects.all()
    return render(request, 'create_examen.html', {'domaine': domaine, 'site_id': site_id, 'classes': classes, 'cours': cours})
        