from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from hospital_Management.models import *
from sitewebpam.models import *
from utilisateurs.models import *
from django.contrib import messages


def create_site_hospital(request, site_id):
    if request.method == "POST":
        title = request.POST.get('title')
        couleur = request.POST.get('couleur')
        logo = request.FILES.get('logo')

        # Récupérer les instances de Sitewebpam correspondantes
        sitewebpam = Sitewebpam.objects.get(id=site_id)
        user = request.user

        # Créer une instances de Site_Hospital_Management avec les données du formulaire
        site_hospital = Site_Hospital_Management.objects.create(
            title=title,
            id_sitepam=sitewebpam,
            Couleur=couleur,
            logo=logo,
        )
        site_hospital.save()

        # Rediriger vers ume nouvelle URL avec les paramètres appropriés
        return redirect('dashboard_hospital', domaine=sitewebpam.domaine)
   


def dashboard_hospital(request, domaine):
    user = request.user
    site = Sitewebpam.objects.filter(id_user=user).first()
    if site:
        site_hospital_info = Site_Hospital_Management.objects.filter(id_sitepam=site).first()
        if site_hospital_info:
            user_info = User_Main.objects.get(username=user.username)
            user_add = Info_utilisateurs.objects.get(id_user=user)
            site_id = site_hospital_info.id
            context = {
                'site_title': site_hospital_info.title,
                'domaine': domaine,
                'site_id': site_id,
                'user_info': user_info,
                'user_add': user_add,
            }
            
            return render(request, 'dashboard_hospital.html', context)   
        else:
            return HttpResponse("No site information found.")
    else:
        return HttpResponse("No site found for the user.")
    
def create_admin_hospital(request, domaine):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les informations du site lié à l'utilisateur connecté
    site = Sitewebpam.objects.filter(id_user=user).first()

    # Vérifier si un site a été trouvé pour l'utilisateur
    if site:
        # Récupérer les informations spécifiques au site à afficher
        site_hospital_info = Site_Hospital_Management.objects.filter(id_sitepam=site).first()
        # Récupérez les informations de l'utilisateur à partir du modèle User_Main
        user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
        site_id = site_hospital_info.id


        # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
        context = {
            'user_info': user_info,
            'site_id': site_id,
            'site_title': site_hospital_info.title,
            'domaine': domaine,
        }
        return render(request, 'create_admin_hospital.html', context)
    else:
        # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
        return HttpResponse("No site found for the user.")
    

#######################################################################################################
# fonction pou ale sou menu an
########################################################################################################

def menu_hospital_doctor(request, domaine):
    # Récupérer l'utilisateur connecté
    user = request.user
    if user.grade == '2':
        # Récupérer le créateur (utilisateur de grade 1)
        creator = user.created_by
        if creator:
            # Récupérer le site lié au créateur
            site = Sitewebpam.objects.filter(id_user=creator).first()
            if site:
                # Récupérer les informations spécifiques au site à afficher
                site_blog_info = Site_Hospital_Management.objects.filter(id_sitepam=site).first()
                # Récupérez les informations de l'utilisateur à partir du modèle User_Main
                user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
                site_id = site_blog_info.id
                # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
                context = {
                    'user_info': user_info,
                    'site_id': site_id,
                    'site_title': site_blog_info.title,
                    'domaine': domaine,
                    'user_grade': user.grade,
                }
                # Logique de vue pour afficher les messages
                return render(request, 'menu_hospital_doctor.html', context)
            else:
                # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
                return HttpResponse("No site found for the user.")
        else:
            # Gérer le cas où le créateur n'est pas trouvé
            return HttpResponse("No creator found for this user.")

    else:
        # Récupérer le site lié à l'utilisateur connecté
        site = Sitewebpam.objects.filter(id_user=user).first()

        # Vérifier si un site a été trouvé pour l'utilisateur
        if site:
            # Récupérer les informations spécifiques au site à afficher
            site_blog_info = Site_Hospital_Management.objects.filter(id_sitepam=site).first()
            # Récupérez les informations de l'utilisateur à partir du modèle User_Main
            user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
            site_id = site_blog_info.id
            # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
            context = {
                'user_info': user_info,
                'site_id': site_id,
                'site_title': site_blog_info.title,
                'domaine': domaine,
            }
            # Logique de vue pour afficher les messages
            return render(request, 'menu_hospital_doctor.html', context)
        else:
            # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
            return HttpResponse("No site found for the user.")

#######################################################################################################
# fonction pou kreye yon nouvo doktè
########################################################################################################

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Sitewebpam, Medecin, Specialite
from django.utils.dateparse import parse_date

# def generate_unique_code(full_name, specialty):
#     import hashlib
#     # Concaténer le nom complet et la spécialité
#     data = f"{full_name}{specialty}"
#     # Créer un hachage MD5 du texte concaténé
#     hash_object = hashlib.md5(data.encode())
#     # Convertir le hachage en une chaîne hexadécimale
#     hex_dig = hash_object.hexdigest()
#     # Prendre les 8 premiers chiffres de la chaîne hexadécimale
#     unique_code = hex_dig[:8]
#     return unique_code.upper()  # Retourner en majuscules pour une meilleure lisibilité

# def create_new_doctor(request, domaine, site_id):
#     # try:
#     # Récupérer l'utilisateur connecté
#     user = request.user
#     if user.grade == '2':
#         # Récupérer le créateur (utilisateur de grade 1)
#         creator = user.created_by
#         if creator:
#             # Récupérer le site lié au créateur
#             site = Sitewebpam.objects.filter(id_user=creator).first()
#             if site:
#                 if request.method == 'POST':
#                     # Récupérer les données du formulaire
#                     nom = request.POST['nom']
#                     prenom = request.POST['prenom']
#                     phone = request.POST['phone']
#                     date_of_birth = request.POST['date_of_birth']
#                     specialite_id = request.POST['specialite']
#                     sexe = request.POST['sexe']
#                     address = request.POST['address']
#                     date_of_admission = request.POST['date_of_admission']
#                     email = request.POST['email']
#                     password = request.POST['password']
#                     confirm_password = request.POST['confirm_password']

#                     if password != confirm_password:
#                         messages.add_message(request, messages.ERROR, 'The password did not match!')
#                         return render(request, 'menu_hospital.html', {'messages': messages.get_messages(request)})
                    
#                     # Générer le code unique
#                     full_name = f"{nom} {prenom}"
#                     specialite = Specialite.objects.get(id=specialite_id)
#                     unique_code = generate_unique_code(full_name, specialite.name)

#                     print(unique_code)

#                     # Traiter les dates
#                     date_of_birth = parse_date(date_of_birth)
#                     date_of_admission = parse_date(date_of_admission)

#                     # Créer et enregistrer le nouveau médecin
#                     medecin = Medecin(
#                         site=site,
#                         code=unique_code,
#                         nom=nom,
#                         prenom=prenom,
#                         sexe=sexe,
#                         tel=phone,
#                         adresse=address,
#                         email=email,
#                         password=password,
#                         specialite=specialite,
#                         date_admission=date_of_admission,
#                         date_of_birth=date_of_birth
#                     )
#                     medecin.save()

#                     # Rediriger après succès
#                     return redirect('dashboard_hospital', domaine=domaine)

#                 else:
#                     # Passer un code temporaire ou un code de test pour le formulaire initial
#                     unique_code = "00000000"
#                     return render(request, 'menu_hospital.html', {'unique_code': unique_code})
#             else:
#                 # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
#                 return HttpResponse("No site found for the user.")
#         else:
#             # Gérer le cas où le créateur n'est pas trouvé
#             return HttpResponse("No creator found for this user.")
#     else:
#         # Récupérer le site lié à l'utilisateur connecté
#         site = Sitewebpam.objects.filter(id_user=user).first()

#         # Vérifier si un site a été trouvé pour l'utilisateur
#         if site:
#             if request.method == 'POST':
#                 # Récupérer les données du formulaire
#                 nom = request.POST['nom']
#                 prenom = request.POST['prenom']
#                 phone = request.POST['phone']
#                 date_of_birth = request.POST['date_of_birth']
#                 specialite_id = request.POST['specialite']
#                 sexe = request.POST['sexe']
#                 address = request.POST['address']
#                 date_of_admission = request.POST['date_of_admission']
#                 email = request.POST['email']
#                 password = request.POST['password']
#                 confirm_password = request.POST['confirm_password']

#                 if password != confirm_password:
#                     messages.add_message(request, messages.ERROR, 'The password did not match!')
#                     return render(request, 'menu_hospital.html', {'messages': messages.get_messages(request)})
                
#                 # Générer le code unique
#                 full_name = f"{nom} {prenom}"
#                 specialite = Specialite.objects.get(id=specialite_id)
#                 unique_code = generate_unique_code(full_name, specialite.name)

#                 # Traiter les dates
#                 date_of_birth = parse_date(date_of_birth)
#                 date_of_admission = parse_date(date_of_admission)

#                 # Créer et enregistrer le nouveau médecin
#                 medecin = Medecin(
#                     site=site,
#                     code=unique_code,
#                     nom=nom,
#                     prenom=prenom,
#                     sexe=sexe,
#                     tel=phone,
#                     adresse=address,
#                     email=email,
#                     password=password,
#                     specialite=specialite,
#                     date_admission=date_of_admission,
#                     date_of_birth=date_of_birth
#                 )
#                 medecin.save()

#                 # Rediriger après succès
#                 return redirect('dashboard_hospital', domaine=domaine)

#             else:
#                 # Passer un code temporaire ou un code de test pour le formulaire initial
#                 unique_code = "00000000"
#                 return render(request, 'menu_hospital.html', {'unique_code': unique_code})
#         else:
#             # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
#             return HttpResponse("No site found for the user.")
#     # except Exception as e:
#     #     error_message = str(e)
#     #     return redirect(reverse('dashboard_hospital', kwargs={'domaine': domaine}) + f'?message={error_message}')


from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

# def create_new_doctor(request, domaine, site_id):
#     user = request.user
#     site = Sitewebpam.objects.filter(id_user=user).first()
#     if site:
#         site_hospital_info = Site_Hospital_Management.objects.filter(id_sitepam=site).first()
#         if site_hospital_info:
#             if request.method == 'POST':
#                 # Récupérer les données du formulaire
#                 nom = request.POST['nom']
#                 prenom = request.POST['prenom']
#                 phone = request.POST['phone']
#                 date_of_birth = request.POST['date_of_birth']
#                 specialite = request.POST['specialite']
#                 sexe = request.POST['sexe']
#                 address = request.POST['address']
#                 date_of_admission = request.POST['date_of_admission']
#                 email = request.POST['email']
#                 password = request.POST['password']
#                 confirm_password = request.POST['confirm_password']

#                 if password != confirm_password:
#                     messages.add_message(request, messages.ERROR, 'The password did not match!')
#                     return render(request, 'menu_hospital.html', {'messages': messages.get_messages(request)})

#                 # Traiter les dates
#                 date_of_birth = parse_date(date_of_birth)
#                 date_of_admission = parse_date(date_of_admission)

#                 # Créer et enregistrer le nouveau médecin
#                 medecin = Medecin(
#                     site=site,
#                     # code=unique_code,
#                     nom=nom,
#                     prenom=prenom,
#                     sexe=sexe,
#                     tel=phone,
#                     adresse=address,
#                     email=email,
#                     password=password,
#                     specialite=specialite,
#                     date_admission=date_of_admission,
#                     date_of_birth=date_of_birth
#                 )
#                 medecin.save()
#                 user_info = User_Main.objects.get(username=user.username)
#                 user_add = Info_utilisateurs.objects.get(id_user=user)
#                 site_id = site_hospital_info.id
#                 context = {
#                     'site_title': site_hospital_info.title,
#                     'domaine': domaine,
#                     'site_id': site_id,
#                     'user_info': user_info,
#                     'user_add': user_add,
#                 }
            
#                 return render(request, 'dashboard_hospital.html', context) 
#                 # Rediriger après succès
#                 # return redirect('dashboard_hospital', domaine=domaine)
#             else:
#                 return render(request, 'menu_hospital.html')
                
#         else:
#             return HttpResponse("No site information found.")
#     else:
#         return HttpResponse("No site found for the user.")


def menu_hospital_speciality(request, domaine):
    # Récupérer l'utilisateur connecté
    user = request.user
    if user.grade == '2':
        # Récupérer le créateur (utilisateur de grade 1)
        creator = user.created_by
        if creator:
            # Récupérer le site lié au créateur
            site = Sitewebpam.objects.filter(id_user=creator).first()
            if site:
                # Récupérer les informations spécifiques au site à afficher
                site_blog_info = Site_Hospital_Management.objects.filter(id_sitepam=site).first()
                # Récupérez les informations de l'utilisateur à partir du modèle User_Main
                user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
                site_id = site_blog_info.id
                # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
                context = {
                    'user_info': user_info,
                    'site_id': site_id,
                    'site_title': site_blog_info.title,
                    'domaine': domaine,
                    'user_grade': user.grade,
                }
                # Logique de vue pour afficher les messages
                return render(request, 'menu_hospital_speciality.html', context)
            else:
                # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
                return HttpResponse("No site found for the user.")
        else:
            # Gérer le cas où le créateur n'est pas trouvé
            return HttpResponse("No creator found for this user.")

    else:
        # Récupérer le site lié à l'utilisateur connecté
        site = Sitewebpam.objects.filter(id_user=user).first()

        # Vérifier si un site a été trouvé pour l'utilisateur
        if site:
            # Récupérer les informations spécifiques au site à afficher
            site_blog_info = Site_Hospital_Management.objects.filter(id_sitepam=site).first()
            # Récupérez les informations de l'utilisateur à partir du modèle User_Main
            user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
            site_id = site_blog_info.id
            # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
            context = {
                'user_info': user_info,
                'site_id': site_id,
                'site_title': site_blog_info.title,
                'domaine': domaine,
            }
            # Logique de vue pour afficher les messages
            return render(request, 'menu_hospital_speciality.html', context)
        else:
            # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
            return HttpResponse("No site found for the user.")

    
    

from django.shortcuts import redirect
from django.urls import reverse

def create_new_doctor(request, domaine, site_id):
    user = request.user
    site = Sitewebpam.objects.filter(id_user=user).first()
    if site:
        site_hospital_info = Site_Hospital_Management.objects.filter(id_sitepam=site).first()
        if site_hospital_info:
            if request.method == 'POST':
                # Récupérer les données du formulaire
                nom = request.POST['nom']
                prenom = request.POST['prenom']
                phone = request.POST['phone']
                date_of_birth = request.POST['date_of_birth']
                specialite = request.POST['specialite']
                sexe = request.POST['sexe']
                address = request.POST['address']
                date_of_admission = request.POST['date_of_admission']
                email = request.POST['email']
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']

                if password != confirm_password:
                    messages.add_message(request, messages.ERROR, 'The password did not match!')
                    return render(request, 'menu_hospital.html', {'messages': messages.get_messages(request)})

                # Traiter les dates
                date_of_birth = parse_date(date_of_birth)
                date_of_admission = parse_date(date_of_admission)

                # Créer et enregistrer le nouveau médecin
                medecin = Medecin(
                    site=site_hospital_info,
                    nom=nom,
                    prenom=prenom,
                    sexe=sexe,
                    tel=phone,
                    adresse=address,
                    email=email,
                    password=password,
                    specialite=specialite,
                    date_admission=date_of_admission,
                    date_of_birth=date_of_birth
                )
                medecin.save()

                # Redirect to dashboard after successful creation
                return redirect(reverse('dashboard_hospital', kwargs={'domaine': domaine}))
            
            else:
                return render(request, 'menu_hospital_doctor.html', {'domaine': domaine})
                
        else:
            return HttpResponse("No site information found.")
    else:
        return HttpResponse("No site found for the user.")
