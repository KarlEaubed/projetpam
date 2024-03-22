from django.contrib.auth.hashers import make_password
from .models import User_Main
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from WebPam import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . tokens import generateToken
from datetime import datetime
from sitewebpam.models import Info_utilisateurs, Sitewebpam
import whois # pip install python-whois
from django.http import JsonResponse


def home(request):
    return render(request, 'index.html')


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
        
        # Vérifiez si le nom d'utilisateur est déjà pris
        if User_Main.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username already taken, please try another.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        # Vérifiez si l'e-mail est déjà associé à un compte
        if User_Main.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'This email is already associated with an account.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        # Vérifiez les contraintes sur le nom d'utilisateur
        if len(username) > 10:
            messages.add_message(request, messages.ERROR, 'Please the username must not be more than 10 characters.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})
        if len(username) < 5:
            messages.add_message(request, messages.ERROR, 'Please the username must be at least 5 characters.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})
        if not username.isalnum():
            messages.add_message(request, messages.ERROR, 'Username must be alphanumeric.')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        # Vérifiez si les mots de passe correspondent
        if password != confirmpwd:
            messages.add_message(request, messages.ERROR, 'The password did not match!')
            return render(request, 'signup.html', {'messages': messages.get_messages(request)})

        # Traitement de la date de naissance
        day = int(request.POST['day'])
        month = int(request.POST['month'])
        year = int(request.POST['year'])
        date_of_birth = datetime(year=int(year), month=int(month), day=int(day))

        # Créez un nouvel utilisateur avec le modèle User_Main
        user = User_Main(
            nom=lastname,
            prenom=firstname,
            username=username,
            email=email,
            password=make_password(password),  # Hachage du mot de passe
            portable=phone,  # Vous pouvez ajuster ceci si nécessaire
            date_de_nais=date_of_birth,
            is_active = False

        )
        user.save()


        messages.add_message(request,messages.SUCCESS, 'Your account has been successfully created. we have sent you an email You must comfirm in order to activate your account.')
        # send email when account has been created successfully
        subject = "Welcome to .WebPam official Website"
        message = "Welcome "+ user.prenom + " " + user.nom + "\n thank for chosing our website to make your own businnes.\n In order to login you need to comfirm your email account.\n thanks\n\n\n .WebPam"
        
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        # send the the confirmation email
        current_site = get_current_site(request) 
        email_suject = "confirm your email .WebPam!"
        messageConfirm = render_to_string("emailConfimation.html", {
            'name': user.prenom,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generateToken.make_token(user)
        })       

        email = EmailMessage(
            email_suject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [user.email]
        )

        email.fail_silently = False
        email.send()
        return render(request, 'signin.html', {'messages': messages.get_messages(request)})

    return render(request, 'signup.html')


def get_initials(user):
    initials = ''
    if user.prenom:
        initials += user.prenom[0].upper()
    if user.nom:
        initials += user.nom[0].upper()
    return initials


def signin(request):
    if request.method == "POST":
        email_username = request.POST['email_username']
        password = request.POST['password']

        # Vérifiez si l'entrée est une adresse email ou un nom d'utilisateur
        if '@' in email_username:
            kwargs = {'email': email_username}
        else:
            kwargs = {'username': email_username}

        # Authentifiez l'utilisateur en fonction de l'email ou du nom d'utilisateur
        user = authenticate(request, **kwargs, password=password)

        if user is not None:
            login(request, user)
            if user.is_active:
                # Vérifiez si l'utilisateur a accepté les conditions d'utilisation
                try:
                    sitewebpam = Sitewebpam.objects.get(id_user=user)
                    if sitewebpam.terms_conditions:
                        return render(request, 'dashboard.html')
                    else:
                        return redirect('finalize_account')
                except Sitewebpam.DoesNotExist:
                    # Si l'utilisateur n'a pas de sitewebpam associé, redirigez-le vers "finalize_account"
                    return redirect('finalize_account')
            else:
                messages.error(request, 'You have not confirmed your email. Please do it in order to activate your account.')
                return render(request, 'signin.html')
        else:
            messages.error(request, 'Bad authentication')
            return render(request, 'signin.html', {'messages': messages.get_messages(request)})

    return render(request, 'signin.html')






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


def logOut(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('home')


def finalize_account(request):
    # Obtenez l'utilisateur connecté
    user = request.user  # Assurez-vous que l'utilisateur est connecté
    # Récupérez les informations de l'utilisateur à partir du modèle User_Main
    user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur

    # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
    context = {
        'user_info': user_info,
    }
    
    # Passez le contexte au modèle HTML
    return render(request, 'finalize_account.html', context)



def setup_account(request):
    if request.method == "POST":
        adresse = request.POST.get('adresse')
        ville = request.POST.get('ville')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        domaine = request.POST.get('domain_name')
        type_abonnement = request.POST.get('type')

        # Vérifier si le domaine est valide
        if domaine:
            try:
                # Interroger les informations WHOIS du domaine
                info_domaine = whois.whois(domaine)
                if info_domaine:
                    user_info = User_Main.objects.get(username=request.user.username)
                    # Créer une instance de Info_utilisateurs avec les données du formulaire
                    user = Info_utilisateurs.objects.create(
                        id_user=user_info,
                        adresse=adresse,
                        ville=ville,
                        state=state,
                        zip_code=zip_code,
                        country=country,
                    )
                    user.save()

                    user_next = Sitewebpam.objects.create(
                        id_user=user_info,
                        domaine=domaine,
                        type=type_abonnement,
                        terms_conditions = True,
                    )
                    user_next.save()


                    # Rediriger l'utilisateur vers la page dashboard.html après avoir créé le compte
                    return render(request, 'dashboard.html')
                else:
                    # Le domaine n'existe pas
                    return render(request, 'finalize_account.html', {'error': 'Domaine non valide'})
            except whois.parser.PywhoisError as e:
                # Erreur lors de la recherche du domaine
                return render(request, 'finalize_account.html', {'error': str(e)})
        else:
            # Aucun domaine spécifié dans le formulaire
            return render(request, 'finalize_account.html', {'error': 'Veuillez spécifier un domaine'})

    return render(request, 'finalize_account.html')




# def update_terms_conditions(request):
#     if request.method == 'POST':
#         # Mettre à jour terms_conditions pour l'utilisateur actuel
#         user = request.user
#         user.sitewebpam.terms_conditions = True
#         user.sitewebpam.save()
        
#         return JsonResponse({'message': 'Terms and conditions updated successfully'})
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
