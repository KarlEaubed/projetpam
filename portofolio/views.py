from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import redirect, render,get_object_or_404
from WebPam import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from datetime import datetime
from sitewebpam.models import Info_utilisateurs, Sitewebpam
from blog.models import *
from portofolio.models import *
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Site_Portofolio
from sitewebpam.models import Sitewebpam
from django.shortcuts import render, redirect, get_object_or_404
from .models import Site_Portofolio, Services_Portofolio
from sitewebpam.models import Sitewebpam
from utilisateurs.models import User_Main  
from .models import Infos_Portofolio, About_Portofolio, Pro_Portofolio, Heroes_Portofolio
from django.http import JsonResponse
from django.shortcuts import render
from .models import Sitewebpam, Site_Portofolio
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Site_Portofolio, Services_Portofolio

# Create your views here.

def create_site_portofolio(request, site_id):
    if request.method == "POST":
        title = request.POST.get('title')
        couleur = request.POST.get('couleur')
        logo = request.FILES.get('logo')

        # Récupérer l'instance de Sitewebpam correspondante
        sitewebpam = Sitewebpam.objects.get(id=site_id)
        
        # Créer une instance de Site_Portofolio avec les données du formulaire
        site_portofolio = Site_Portofolio.objects.create(
            title=title,
            id_sitepam=sitewebpam,
            couleur=couleur,
            logo=logo,
            site_id=site_id  # Assurez-vous d'inclure la valeur de site_id ici
        )

        # Rediriger vers le tableau de bord du portefeuille
        return redirect('dashboardportofolio', domaine=sitewebpam.domaine)

    return render(request, 'create_site_portofolio.html', {'site_id': site_id})



# Dashboard portofolio


    





def dashboardportofolio(request, domaine):
    portofolios = Site_Portofolio.objects.filter(id_sitepam__domaine=domaine)
    if portofolios.exists():
        portofolio = portofolios.first()
        sitewebpam = portofolio.id_sitepam
        site_id = sitewebpam.id  # Récupérer l'ID du site

        # Nombre de services
        nombre_services = Services_Portofolio.objects.filter(site=portofolio).count()

        # Nombre de compétences (skills)
        nombre_skills = Skill_Portofolio.objects.filter(site=portofolio).count()

        # Nombre de projets (pro)
        nombre_projets = Pro_Portofolio.objects.filter(site=portofolio).count()

        return render(request, 'dashboardportoo.html', {
            'domaine': domaine,
            'portofolio': portofolio,
            'sitewebpam': sitewebpam,
            'site_id': site_id,
            'nombre_services': nombre_services,
            'nombre_skills': nombre_skills,
            'nombre_projets': nombre_projets
        })
    else:
        return render(request, 'erreur.html', {'message': 'Aucun portefeuille trouvé pour ce domaine.'})


    
    
    
def view_site_portofolio(request, domaine):
    # Récupérer le site portofolio à partir du domaine donné
    site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam__domaine=domaine)
    

    # Récupérer les informations nécessaires sur le site portofolio
    title = site_portofolio.title
    couleur = site_portofolio.couleur
    logo = site_portofolio.logo

    # Récupérer les informations additionnelles du site portofolio
    infos = Infos_Portofolio.objects.filter(site=site_portofolio)
    about = About_Portofolio.objects.filter(site=site_portofolio).first()  
    services = Services_Portofolio.objects.filter(site=site_portofolio)
    heroes = Heroes_Portofolio.objects.filter(site=site_portofolio)
    carrieres = Carriere_Portofolio.objects.filter(site=site_portofolio)
    etudes = Etude_Portofolio.objects.filter(site=site_portofolio)
    skills = Skill_Portofolio.objects.filter(site=site_portofolio)


    # Récupérer les projets portofolio associés à ce site
    pro = Pro_Portofolio.objects.filter(site=site_portofolio)

    # Passer les données au template
    return render(request, 'view_site_portofolio.html', {
        'title': title,
        'logo': logo,
        'couleur': couleur,
        'sitewebpam': site_portofolio.id_sitepam,  
        'infos': infos,
        'about': about,
        'services': services,
        'heroes' : heroes,
        'pro': pro,
        'carrieres':carrieres,
        'etudes': etudes,
        'skills': skills,
        'site_id': site_portofolio.id,
        
    })
    
    
   
    



def add_service(request, domaine, site_id):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        image = request.FILES.get('image')
        descriptions = request.POST.get('descriptions')
        autres = request.POST.get('autres')

        # Obtenez l'instance de Sitewebpam correspondant à partir de site_id
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

        # Obtenez l'instance de SitePortofolio associée au Sitewebpam
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)
        

        # Créez le service en l'associant au SitePortofolio correspondant
        service = Services_Portofolio.objects.create(
            site=site_portofolio,
            titre=titre,
            image=image,
            descriptions=descriptions,
            autres=autres
        )
        service.save()
        # Rediriger vers la page de détail du site_portofolio
        return redirect('add_service', site_id=site_portofolio.pk, domaine=domaine)
    else:
        # Obtenez tous les services associés au site_portofolio actuel
        services = Services_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'add_service.html', {'site_id': site_id, 'services': services, 'domaine': domaine})
    
    
    
def view_service(request, domaine, site_id):
    
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)
        
        # Affichage pour le débogage
        print(f"site_id: {site_id}")
        print(f"domaine: {domaine}")

        # Obtenez l'instance de SitePortofolio associée au Sitewebpam
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)
        # Obtenez tous les services associés au site_portofolio actuel
        services = Services_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'view_service.html', {'site_id': site_id, 'services': services, 'domaine': domaine})
    
    
    
def modif_service(request, service_id):
    # Récupérer le service à modifier
    service = get_object_or_404(Services_Portofolio, pk=service_id)
    site_id = service.site.id_sitepam.id  # Extraire l'ID de sitewebpam

    if request.method == 'POST':
        # Traiter le formulaire de modification du service
        service.titre = request.POST.get('titre')
        service.descriptions = request.POST.get('descriptions')
        if 'image' in request.FILES:
            service.image = request.FILES.get('image')
        service.save()

        # Rediriger vers la page d'ajout de service avec le site_id
        return redirect('add_service', site_id=site_id)

    # Si la méthode HTTP est GET, afficher le formulaire de modification du service
    return render(request, 'modifservice.html', {'service': service})







# Def pou Infos #########################################################3
def add_info(request, domaine, site_id):
    info_exists = Infos_Portofolio.objects.filter(site__id_sitepam=site_id).exists()

    if request.method == 'POST':
        if not info_exists:
            # Récupérer les données du formulaire
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            adresse = request.POST.get('adresse')
            location = request.POST.get('location')

            sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

            # Obtenez l'instance de SitePortofolio associée au Sitewebpam
            site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)

            # Créer une nouvelle instance d'Infos_Portofolio en utilisant l'instance site_portofolio
            infos = Infos_Portofolio.objects.create(
                site=site_portofolio,  # Utilisez l'instance site_portofolio ici
                nom=nom,
                prenom=prenom,
                phone=phone,
                email=email,
                adresse=adresse,
                location=location
            )
            # Rediriger vers une autre vue ou une page de confirmation
            return redirect('view_info', site_id=site_id, domaine=domaine)
        else:
            # Afficher un message d'erreur
            messages.error(request, "Un objet Info_Portofolio existe déjà pour ce Site_Portofolio.")
            # Rediriger vers la même vue
            return redirect('view_info', site_id=site_id)
    else:
        # Obtenez tous les services associés au site_portofolio actuel
        infos = Infos_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'add_info.html', {'site_id': site_id, 'infos': infos, 'domaine': domaine})
    
    
    
    
def view_info(request, domaine, site_id):

        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

            # Obtenez l'instance de SitePortofolio associée au Sitewebpam
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)
        # Obtenez tous les services associés au site_portofolio actuel
        infos = Infos_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'view_info.html', {'site_id': site_id, 'infos': infos, 'domaine': domaine})





# def pour l'About  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4

def add_about(request, domaine, site_id):
    # Vérifier s'il existe déjà un objet About_Portofolio associé à ce Site_Portofolio
    about_exists = About_Portofolio.objects.filter(site__id_sitepam=site_id).exists()
    
    if request.method == 'POST':
        if not about_exists:  # Vérifier s'il n'existe pas déjà d'objet About_Portofolio
            # Récupérer les données du formulaire
            texte = request.POST.get('texte')
            autre = request.POST.get('autre')
            image = request.FILES.get('image')

            # Obtenez l'instance de Sitewebpam correspondant à partir de site_id
            sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

            # Obtenez l'instance de SitePortofolio associée au Sitewebpam
            site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)

            # Créer une nouvelle instance d'About_Portofolio en utilisant l'instance site_portofolio
            about = About_Portofolio.objects.create(
                site=site_portofolio,  # Utilisez site_portofolio au lieu de site_id
                texte=texte,
                autre=autre,
                image=image
            )
            about.save()
            # Rediriger vers une autre vue ou une page de confirmation
            return redirect('add_about', site_id=site_id, domaine=domaine)
        else:
                        # Afficher un message d'erreur
            messages.error(request, "Un objet About_Portofolio existe déjà pour ce Site_Portofolio.")
            # Rediriger vers la même vue
            return redirect('add_about', site_id=site_id)

    else:
                # Obtenez tous les services associés au site_portofolio actuel
        abouts = About_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'add_about.html', {'site_id': site_id, 'abouts': abouts, 'domaine': domaine})




    





# Ajoute projet ##################################################################################################
def add_pro(request, domaine, site_id):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.POST.get('titre')
        descriptions = request.POST.get('descriptions')
        image = request.FILES.get('image')
        created_at = request.POST.get('created_at')
        links = request.POST.get('links')
        categorie = request.POST.get('categorie')
        
        # Obtenez l'instance de Sitewebpam correspondant à partir de site_id
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

        # Obtenez l'instance de SitePortofolio associée au Sitewebpam
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)
        
        # Créer une nouvelle instance de Pro_Portofolio en utilisant l'instance site_portofolio
        pro = Pro_Portofolio.objects.create(
            site=site_portofolio,  # Utilisez site_portofolio au lieu de site_id
            titre=titre,
            descriptions=descriptions,
            image=image,
            created_at=created_at,
            links=links,
            categorie=categorie
        )
        # Rediriger vers une autre vue ou une page de confirmation
        return redirect('add_pro', site_id=site_id, domaine=domaine)
    else:
                # Obtenez tous les services associés au site_portofolio actuel
        pros = Pro_Portofolio.objects.filter(site__id_sitepam=site_id)

        # Renvoyer le formulaire d'ajout de service et la liste des services existants
        return render(request, 'add_pro.html', {'site_id': site_id, 'pros': pros, 'domaine': domaine})

    
    
    
    
    
# pou heroooooooo
def add_hero(request, domaine, site_id):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre1 = request.POST.get('titre1')
        titre2 = request.POST.get('titre2')
        paragraphe = request.POST.get('paragraphe')
        cv = request.POST.get('cv')
        image = request.FILES.get('image')
        
        # Obtenez l'instance de Sitewebpam correspondant à partir de site_id
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

        # Obtenez l'instance de SitePortofolio associée au Sitewebpam
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)

        # Créer une nouvelle instance de Heroes_Portofolio en utilisant l'instance site_portofolio
        hero = Heroes_Portofolio.objects.create(
            site=site_portofolio,  # Utilisez l'instance site_portofolio ici
            titre1=titre1,
            titre2=titre2,
            paragraphe=paragraphe,
            cv=cv,
            image=image
        )
        # Rediriger vers une autre vue ou une page de confirmation
        return redirect('add_about', site_id=site_id, domaine=domaine)
    else:
        # Afficher le formulaire d'ajout d'infos
        return render(request, 'add_hero.html', {'site_id': site_id, 'domaine': domaine})
    
    
    
    
    
def add_carriere(request, domaine, site_id):
    if request.method == 'POST':
        poste = request.POST.get('poste')
        compagnie = request.POST.get('compagnie')
        description = request.POST.get('description')
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

        # Obtenez l'instance de SitePortofolio correspondant à partir de site_id
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=site_id)

        # Créez l'objet Carriere_Portofolio associé au SitePortofolio correspondant
        carriere = Carriere_Portofolio.objects.create(
            site=site_portofolio,
            poste=poste,
            compagnie=compagnie,
            description=description,
            debut=debut,
            fin=fin
        )
        carriere.save()
       
        return redirect('add_carriere', site_id=site_portofolio.pk, domaine=domaine)
    else:
        
        carrieres = Carriere_Portofolio.objects.filter(site__id_sitepam=site_id)

        return render(request, 'add_carriere.html', {'site_id': site_id, 'carrieres': carrieres, 'domaine': domaine})
    
    
    
    
    
def add_etude(request, domaine, site_id):
    if request.method == 'POST':
        domaine = request.POST.get('domaine')
        ecole = request.POST.get('ecole')
        description = request.POST.get('description')
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        
        
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

       
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=site_id)

       
        etude = Etude_Portofolio.objects.create(
            site=site_portofolio,
            domaine=domaine,
            ecole=ecole,
            description=description,
            debut=debut,
            fin=fin
        )
        etude.save()
      
        return redirect('add_etude', site_id=site_portofolio.pk, domaine=domaine)
    else:
     
        etudes = Etude_Portofolio.objects.filter(site__id_sitepam=site_id)


        return render(request, 'add_etude.html', {'site_id': site_id, 'etudes': etudes, 'domaine': domaine})
    
    
    
    
def add_skill(request, domaine, site_id):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        pourcentage = request.POST.get('pourcentage')
        
        
        
        sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)

        
        site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=site_id)

        skill = Skill_Portofolio.objects.create(
            site=site_portofolio,
            nom=nom,
            description=description,
            pourcentage=pourcentage
        )
        skill.save()
    
        return redirect('add_skill', site_id=site_portofolio.pk, domaine= domaine)
    else:
        
        skills = Skill_Portofolio.objects.filter(site__id_sitepam=site_id)

   
        return render(request, 'add_skill.html', {'site_id': site_id, 'skills': skills, 'domaine': domaine})







@csrf_exempt
def send_email(request, site_id):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nomComplet = request.POST.get('nometprenom')
        email_visitor = request.POST.get('email')
        
        service_titre = request.POST.get('service')
        message = request.POST.get('contenu')
        budget = request.POST.get('budget')

        # Obtenez l'instance de Site_Portofolio correspondant à partir de site_id
        site_portofolio = get_object_or_404(Site_Portofolio, id=site_id)

        # Récupérer l'objet Infos_Portofolio associé au site
        infos_portofolio = get_object_or_404(Infos_Portofolio, site=site_portofolio)

        # Obtenez l'email du propriétaire du site à partir de l'objet Infos_Portofolio
        email_proprio = infos_portofolio.email

        # Obtenez le titre du service à partir de son ID
        
        
        service = get_object_or_404(Services_Portofolio, titre=service_titre)

        # Envoyer l'email
        send_mail(
            f"Demande de service: {service.titre}",
            f"Nom et Prénom: {nomComplet}\nEmail: {email_visitor}\nService: {service.titre}\nMessage: {message}\nBudget: {budget}",
            email_visitor,
            [email_proprio],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Email envoyé avec succès.'})
    else:
        # Gérer les autres méthodes HTTP
        return JsonResponse({'message': 'Méthode non autorisée.'}, status=405)
    
    
    
    
    
    
    

@csrf_exempt
def send_whatsapp(request, site_id):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nomComplet = request.POST.get('nometprenom')
        whatsapp_number = request.POST.get('whatsapp')
        service_titre = request.POST.get('service')
        message = request.POST.get('contenu')
        budget = request.POST.get('budget')

        # Obtenez l'instance de Site_Portofolio correspondant à partir de site_id
        site_portofolio = get_object_or_404(Site_Portofolio, id=site_id)

        # Récupérer l'objet Infos_Portofolio associé au site
        infos_portofolio = get_object_or_404(Infos_Portofolio, site=site_portofolio)

        # Obtenez le numéro de téléphone du propriétaire du site à partir de l'objet Infos_Portofolio
        phone_proprio = infos_portofolio.phone

        # Construire le message WhatsApp
        whatsapp_message = f"Nom et Prénom: {nomComplet}\n Numéro WhatsApp: {whatsapp_number}\n Service: {service_titre}\n Message: {message}\n Budget: {budget}"
        whatsapp_url = f"https://wa.me/{phone_proprio}?text={whatsapp_message}"

        return JsonResponse({'whatsapp_url': whatsapp_url})
    else:
        # Gérer les autres méthodes HTTP
        return JsonResponse({'message': 'Méthode non autorisée.'}, status=405)
    
    
    
    
    
    
def contact_view(request, site_id):
    # Récupérer les services liés au site
    site_portofolio = get_object_or_404(Site_Portofolio, pk=site_id)
    services = Services_Portofolio.objects.filter(site=site_portofolio)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nomComplet = request.POST.get('nometprenom')
        email_visitor = request.POST.get('email')
        service_id = request.POST.get('service')
        demande = request.POST.get('demande')
        budget = request.POST.get('budget')

        # Obtenez le service sélectionné
        service = get_object_or_404(Services_Portofolio, pk=service_id)

        # Récupérer l'email du propriétaire du site à partir de l'objet Infos_Portofolio
        infos_portofolio = get_object_or_404(Infos_Portofolio, site=site_portofolio)
        email_proprio = infos_portofolio.email

        # Envoyer l'email
        send_mail(
            f"Demande de contact pour le service: {service.titre}",
            f"Nom et Prénom: {nomComplet}\nEmail: {email_visitor}\nService: {service.titre}\nDemande: {demande}\nBudget: {budget}",
            email_visitor,
            [email_proprio],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Email envoyé avec succès.'})

    return render(request, 'contact.html', {'site_id': site_id, 'services': services})




def design_site(request, domaine, site_id):
    site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=site_id)
    design, created = Design_Site_Portofolio.objects.get_or_create(site=site_portofolio)

    if request.method == 'POST':
        design.navbar_choice = request.POST.get('navbar_choice')
        design.header_choice = request.POST.get('header_choice')
        design.about_choice = request.POST.get('about_choice')
        design.service_choice = request.POST.get('service_choice')
        design.skill_choice = request.POST.get('skill_choice')
        design.experience_choice = request.POST.get('experience_choice')
        design.projet_choice = request.POST.get('projet_choice')
        design.contact_choice = request.POST.get('contact_choice')
        design.footer_choice = request.POST.get('footer_choice')
        design.save()

        return redirect('design_site', domaine=domaine, site_id=site_id)

    return render(request, 'design_site.html', {
        'site_id': site_id,
        'design': design,
        'domaine': domaine
    })
    
    
    
    
    
def main_view(request, domaine, site_id):
    sitewebpam = get_object_or_404(Sitewebpam, pk=site_id)
    site_portofolio = get_object_or_404(Site_Portofolio, id_sitepam=sitewebpam)
    
     # Récupérer les informations nécessaires sur le site portofolio
    title = site_portofolio.title
    couleur = site_portofolio.couleur
    logo = site_portofolio.logo
    
    
    infos = Infos_Portofolio.objects.filter(site=site_portofolio)
    about = About_Portofolio.objects.filter(site=site_portofolio).first()  
    services = Services_Portofolio.objects.filter(site=site_portofolio)
    heroes = Heroes_Portofolio.objects.filter(site=site_portofolio)
    carrieres = Carriere_Portofolio.objects.filter(site=site_portofolio)
    etudes = Etude_Portofolio.objects.filter(site=site_portofolio)
    skills = Skill_Portofolio.objects.filter(site=site_portofolio)
    pro = Pro_Portofolio.objects.filter(site=site_portofolio)

    design, created = Design_Site_Portofolio.objects.get_or_create(site=site_portofolio)

    # Vérifiez si les valeurs existent, sinon définissez-les à None ou à une valeur temporaire pour le débogage
    design.navbar_choice = design.navbar_choice if design.navbar_choice else 'navbar1.html'
    design.header_choice = design.header_choice if design.header_choice else 'header1.html'
    design.about_choice = design.about_choice if design.about_choice else 'about1.html'
    design.service_choice = design.service_choice if design.service_choice else 'service1.html'
    design.skill_choice = design.skill_choice if design.skill_choice else 'skill1.html'
    design.experience_choice = design.experience_choice if design.experience_choice else 'experience1.html'
    design.projet_choice = design.projet_choice if design.projet_choice else 'projet1.html'
    design.contact_choice = design.contact_choice if design.contact_choice else 'contact1.html'
    design.footer_choice = design.footer_choice if design.footer_choice else 'footer1.html'

    return render(request, 'main_view.html', {'design': design,
                                              'domaine': domaine,
                                              'site_id': site_id,
                                                'title': title,
                                                'logo': logo,
                                                'couleur': couleur,
                                                'sitewebpam': site_portofolio.id_sitepam,  
                                                'infos': infos,
                                                'about': about,
                                                'services': services,
                                                'heroes' : heroes,
                                                'pro': pro,
                                                'carrieres':carrieres,
                                                'etudes': etudes,
                                                'skills': skills,
                                                'site_id': site_portofolio.id,
                                              })





