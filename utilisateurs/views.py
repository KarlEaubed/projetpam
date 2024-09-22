from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from hospital_Management.models import Site_Hospital_Management
from .models import User_Main
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import redirect, render,get_object_or_404
from django.core.mail import send_mail, EmailMessage
from WebPam import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import generateToken
from datetime import datetime
from sitewebpam.models import Info_utilisateurs, Sitewebpam
from blog.models import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import moncashify
from sitewebpam.models import Plan
from django.http import JsonResponse
import json

#######################################################################################################
# Fonction test pou paypal la
#######################################################################################################
def home(request):
    plans = Plan.objects.all()
    context = {'plans' : plans}
    return render(request, 'index.html', context)

def checkout(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id)
    context = {'plan': plan}
    return render(request, 'checkout.html', context)

def paymentcomplete(request, plan_id):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_info = User_Main.objects.get(username=request.user.username)
            plan = Plan.objects.get(id=body['planId'])
            plan_name = get_object_or_404(Plan, pk=plan_id)
            type_abonnement = plan_name.name  # Récupérez le nom du plan

            # Calcul de date_fin en fonction de date_debut
            date_debut = timezone.now()  # Supposons que c'est la date de début
            date_fin = date_debut + timezone.timedelta(days=365)

            # Création de l'objet Abonement avec les valeurs requises
            Abonement.objects.create(
                id_user=user_info,
                plan=plan,
                type_abonnement=type_abonnement,
                date_debut=date_debut,
                date_fin=date_fin,
            )
            return JsonResponse('Payment completed!', safe=False)
        except (KeyError, User_Main.DoesNotExist, Plan.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

#######################################################################################################
# Fonction pou itilizatè prensipal la kreye yon kont
#######################################################################################################

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmpwd = request.POST['confirmpassword']
        day = request.POST['day']
        month = request.POST['month']
        year = request.POST['year']
        
        if User_Main.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username already taken, please try another.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        if User_Main.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'This email is already associated with an account.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        if not username.isalnum():
            messages.add_message(request, messages.ERROR, 'Username must be alphanumeric.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        if password != confirmpwd:
            messages.add_message(request, messages.ERROR, 'The password did not match!')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        day = int(request.POST['day'])
        month = int(request.POST['month'])
        year = int(request.POST['year'])
        date_of_birth = datetime(year=int(year), month=int(month), day=int(day))

        user = User_Main(
            nom=lastname,
            prenom=firstname,
            username=username,
            email=email,
            password=make_password(password),
            portable=phone,
            date_de_nais=date_of_birth,
            grade="1",
            is_active = True,
        )
        user.save()
        setup_account(request)

        # messages.add_message(request,messages.SUCCESS, 'Your account has been successfully created. we have sent you an email You must comfirm in order to activate your account.')
        
        # subject = "Welcome to .WebPam official Website"
        # message = "Welcome "+ user.prenom + " " + user.nom + "\n thank for chosing our website to make your own businnes.\n In order to login you need to comfirm your email account.\n thanks\n\n\n .WebPam"
        
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [user.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        # current_site = get_current_site(request) 
        # email_suject = "confirm your email .WebPam!"
        # messageConfirm = render_to_string("emailConfimation.html", {
        #     'name': user.prenom,
        #     'domain':current_site.domain,
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': generateToken.make_token(user)
        # })       

        # email = EmailMessage(
        #     email_suject,
        #     messageConfirm,
        #     settings.EMAIL_HOST_USER,
        #     [user.email]
        # )

        # email.fail_silently = False
        # email.send()
        # return render(request, 'signin.html', {'messages': messages.get_messages(request)})

    return render(request, 'signup.html')

#######################################################################################################
# Fonction pou itilizatè prensipal la konekte sou kont li
#######################################################################################################

@csrf_protect
def signin(request):
    if request.method == "POST":
        email_username = request.POST['email_username']
        password = request.POST['password']

        if '@' in email_username:
            kwargs = {'email': email_username}
        else:
            kwargs = {'username': email_username}

        user = authenticate(request, **kwargs, password=password)        

        if user is not None:
            login(request, user)
            if user.is_active:
                user_info = User_Main.objects.get(username=user.username)
                context = {'user_info': user_info}

                if user_info.grade == '1':
                    try:
                        sitewebpam = Info_utilisateurs.objects.get(id_user=user)
                        sitewebpam_type = Sitewebpam.objects.get(id_user=user)
                        domaine = sitewebpam_type.domaine

                        if sitewebpam.terms_conditions:
                            if sitewebpam_type.type == 'blog':
                                return redirect('dashboard_blog', domaine=domaine)
                            elif sitewebpam_type.type == 'portfolio':
                                return redirect('dashboardportofolio', domaine=domaine)
                            elif sitewebpam_type.type == 'school_Management':
                                return redirect('dashboard_school', domaine=domaine)
                            elif sitewebpam_type.type == 'hospital_Management':
                                return redirect('dashboard_hospital', domaine=domaine)
                        else:
                            return render(request, 'finalize_account.html', context)
                    except Info_utilisateurs.DoesNotExist:
                        return render(request, 'finalize_account.html', context)

                elif user_info.grade == '2':
                    if user_info.created_by:
                        try:
                            creator_info = Info_utilisateurs.objects.get(id_user=user_info.created_by)
                            domaine = Sitewebpam.objects.get(id_user=user_info.created_by).domaine
                            return redirect('dashboard_blog', domaine=domaine)
                        except Info_utilisateurs.DoesNotExist:
                            messages.error(request, 'Creator info not found.')
                            return render(request, 'signin.html', {'messages': messages.get_messages(request)})
                    else:
                        messages.error(request, 'No creator found for this user.')
                        return render(request, 'signin.html', {'messages': messages.get_messages(request)})

                else:
                    messages.error(request, 'Invalid user grade.')
                    return render(request, 'signin.html', {'messages': messages.get_messages(request)})
            else:
                messages.error(request, 'You have not confirmed your email. Please do it in order to activate your account.')
                return render(request, 'signin.html')
        else:
            messages.error(request, 'Bad authentication')
            return render(request, 'signin.html', {'messages': messages.get_messages(request)})

    return render(request, 'signin.html')

#######################################################################################################
# Fonction pou aktive yon kont
#######################################################################################################

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User_Main.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User_Main.DoesNotExist):
        user = None

    if user is not None and generateToken.check_token(user, token):
        user.is_active  = True        
        user.save()
        messages.add_message(request,messages.SUCCESS, "You are account is activated you can login by filling the form below.")
        return render(request,"signin.html",{'messages':messages.get_messages(request)})
    else:
        messages.add_message(request,messages.ERROR, 'Activation failed please try again')
        return render(request,'index.html',{'messages':messages.get_messages(request)})

#######################################################################################################
# Fonction pou itilizatè prensipal la dekonekte de kont li
#######################################################################################################

def logOut(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('home')

#######################################################################################################
# Fonction pou itilizatè prensipal la antre lòt enfòmasyon adisyonèl
#######################################################################################################

@login_required
def setup_account(request):
    if request.method == "POST":
        adresse = request.POST.get('adresse')
        ville = request.POST.get('ville')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        image = request.FILES.get('profile_image')

        user_info = User_Main.objects.get(username=request.user.username)
        nom = user_info.nom
        prenom = user_info.prenom

        # Récupérer la première lettre du nom et du prénom
        first_letter_firstname = nom[0].upper() if nom else ''
        first_letter_lastname = prenom[0].upper() if prenom else ''

        # Concaténer les initiales
        initials = first_letter_firstname + first_letter_lastname

        # Créer une instance de Info_utilisateurs avec les données du formulaire
        user = Info_utilisateurs.objects.create(
            id_user=user_info,
            adresse=adresse,
            ville=ville,
            state=state,
            zip_code=zip_code,
            country=country,
            terms_conditions=True,
            image=image,
            initials=initials  # Enregistrer les initiales dans le champ correspondant
        )
        user.save()
        # Rediriger l'utilisateur vers la page dashboard.html après avoir créé le compte
        return render(request, 'site.html')

    return render(request, 'finalize_account.html')

#######################################################################################################
# Fonction pou rekipere inisyal itilizatè prensipal la 
#######################################################################################################

def get_initials(user):
    initials = ''
    if user.prenom:
        initials += user.prenom[0].upper()
    if user.nom:
        initials += user.nom[0].upper()
    return initials

#######################################################################################################
# fontion pou kreye site WebPam lan
#######################################################################################################

def site_creation(request):
    if request.method == "POST":
        domaine = request.POST.get('domaine')
        nom_site = request.POST.get('nom_site')
        type_site = request.POST.get('type_site')
        stockage = request.POST.get('stockage')

        user = request.user

        # Ajout de ".webpam" au nom de domaine fourni par l'utilisateur
        domaine = domaine.strip() + '.webpam'

        # Vérifier si le nom de domaine est unique
        if Sitewebpam.objects.filter(domaine=domaine).exists():
            # Si le nom de domaine existe déjà, renvoyer un message d'erreur et afficher la page de création de site
            error_message = 'Ce nom de domaine est déjà utilisé.'
            return render(request, 'site.html', {'error_message': error_message})

        # Créer un nouveau site WebPam avec les informations fournies
        sitewebpam = Sitewebpam.objects.create(
            id_user=user,
            domaine=domaine,
            nom_site=nom_site,
            type=type_site,
            stockage=stockage
        )
        
        if type_site == 'blog':
            # Vérifier si l'ID du site est valide
            if sitewebpam.id:
                # Rediriger vers la vue create_admin_blog, en passant l'ID du site dans les paramètres d'URL
                return render(request, 'createsite.html', {'site_id': sitewebpam.id})

            else:
                # Si l'ID du site est vide ou inexistant, afficher un message d'erreur ou rediriger vers une autre vue
                error_message = 'Invalid site ID.'
                return render(request, 'site.html', {'error_message': error_message})
            
        elif type_site == 'portfolio':
            # Rediriger vers la vue create_site_portofolio, en passant l'ID du site dans les paramètres d'URL
            if sitewebpam.id:
                # Rediriger vers la vue create_admin_blog, en passant l'ID du site dans les paramètres d'URL
                return redirect('create_site_portofolio', site_id=sitewebpam.id)

            else:
                # Si l'ID du site est vide ou inexistant, afficher un message d'erreur ou rediriger vers une autre vue
                error_message = 'Invalid site ID.'
                return render(request, 'site.html', {'error_message': error_message})
            
        elif type_site == "school_Management":
            if sitewebpam.id:
                # Rediriger vers la vue create_admin_blog, en passant l'ID du site dans les paramètres d'URL
                return render(request, 'create_site_school.html', {'site_id': sitewebpam.id})

            else:
                # Si l'ID du site est vide ou inexistant, afficher un message d'erreur ou rediriger vers une autre vue
                error_message = 'Invalid site ID.'
                return render(request, 'site.html', {'error_message': error_message})
        elif type_site == "hospital_Management":
            if sitewebpam.id:
                return render(request, 'create_site_hospital.html', {'site_id': sitewebpam.id})
            
            else:
                # Si l'ID du site est vide ou inexistant, afficher un message d'erreur ou rediriger vers une autre vue
                error_message = 'Invalid site ID.'
                return render(request, 'site.html', {'error_message': error_message})
           
           
       

    return render(request, 'site.html')

#######################################################################################################
# fonction pou kreye site blog lan
# #######################################################################################################

def create_site_blog(request, site_id):

    if request.method == "POST":
        title = request.POST.get('title')
        couleur = request.POST.get('couleur')
        logo = request.FILES.get('logo')

        # Récupérer les instances de Sitewebpam et Admin_Blog correspondantes
        sitewebpam = Sitewebpam.objects.get(id=site_id)
        user = request.user

        # Créer une instance de Site_Blog avec les données du formulaire
        site_blog = Site_Blog.objects.create(
            title=title,
            id_sitepam=sitewebpam,
            id_Admin_Blog=user,
            Couleur=couleur,
            logo=logo
        )
        site_blog.save()


        # Rediriger vers une nouvelle URL avec les paramètres appropriés
        return redirect('dashboard_blog', domaine=sitewebpam.domaine) # Assurez-vous d'avoir la bonne URL ici

    # Dans votre vue Django
    return render(request, 'createsite.html', {'site_id': site_id})


#######################################################################################################
# fonction test pou moncash
# #######################################################################################################

def payment_moncash(request):
    client_id = 'c2a21c8902bb5dce61eed3ff44d57337'
    client_secret = 'oHrr4tbnB1PH0uz6VQNUvVcLYdY8adw-ERjh7xdgANuUQHV-uUXIw8oc8BJsBupj'

    debug = True
    moncash = moncashify.API(client_id, client_secret, debug)

    # payment
    order_id = 'Tennis 023'
    price = 2500 #HTG
    payment = moncash.payment(order_id, price)

    redirect_url = payment.redirect_url

    print('URL:', redirect_url)

    return redirect(redirect_url)


