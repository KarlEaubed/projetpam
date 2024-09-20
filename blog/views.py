from django.shortcuts import get_object_or_404, render, redirect
from WebPam import settings
from sitewebpam.models import Sitewebpam
from blog.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
import os
import requests
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re

# Vue de l'application "blog"

#######################################################################################################
# fonction pou ale sou dashboard lan
########################################################################################################

def dashboard_blog(request, domaine):
    user = request.user

    if user.grade == '2':
        creator = user.created_by
        if creator:
            site = Sitewebpam.objects.filter(id_user=creator).first()
            if site:
                site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
                if site_blog_info:
                    post_count = Post_Blog.objects.filter(site=site_blog_info).count()
                    comment_count = Comment_Blog.objects.filter(post__site=site_blog_info).count()
                    like_count = Like_Blog.objects.filter(post__site=site_blog_info).count()
                    user_count = User_Standard.objects.filter(site=site_blog_info).count()
                    user_standards = User_Standard.objects.filter(site=site_blog_info)
                    
                    # Conversion de user_standards en une liste d'IDs d'utilisateurs
                    user_standard_ids = user_standards.values_list('id', flat=True)
                    likes_count = Like_Blog.objects.filter(user_id__in=user_standard_ids).count()
                    
                    user_info = User_Main.objects.get(username=user.username)
                    user_add = Info_utilisateurs.objects.get(id_user=creator)
                    unread_notifications_count = Notification.objects.filter(site=site_blog_info, is_read=False).count()
                    notifications = Notification.objects.filter(site=site_blog_info).order_by('-created_at')[:5]

                    site_id = site_blog_info.id
                    context = {
                        'post_count': post_count,
                        'comment_count': comment_count,
                        'like_count': like_count,
                        'site_title': site_blog_info.title,
                        'domaine': site.domaine,
                        'site_id': site_id,
                        'user_info': user_info,
                        'user_add': user_add,
                        'user_count': user_count,
                        'user_grade': user.grade,
                        'unread_notifications_count': unread_notifications_count,
                        'notifications': notifications,
                        'user_standards': user_standards,
                        'likes_count': likes_count,
                    }
                    return render(request, 'dashboard_blog.html', context)
                else:
                    return HttpResponse("No site information found.")
            else:
                return HttpResponse("No site found for the user.")
        else:
            return HttpResponse("No creator found for this user.")
    else:
        site = Sitewebpam.objects.filter(id_user=user).first()
        if site:
            site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
            if site_blog_info:
                post_count = Post_Blog.objects.filter(site=site_blog_info).count()
                comment_count = Comment_Blog.objects.filter(post__site=site_blog_info).count()
                like_count = Like_Blog.objects.filter(post__site=site_blog_info).count()
                user_count = User_Standard.objects.filter(site=site_blog_info).count()
                user_standards = User_Standard.objects.filter(site=site_blog_info)
                
                # Conversion de user_standards en une liste d'IDs d'utilisateurs
                user_standard_ids = user_standards.values_list('id', flat=True)
                likes_count = Like_Blog.objects.filter(user_id__in=user_standard_ids).count()
                
                user_info = User_Main.objects.get(username=user.username)
                user_add = Info_utilisateurs.objects.get(id_user=user)
                unread_notifications_count = Notification.objects.filter(site=site_blog_info, is_read=False).count()
                notifications = Notification.objects.filter(site=site_blog_info).order_by('-created_at')[:5]

                site_id = site_blog_info.id
                context = {
                    'post_count': post_count,
                    'comment_count': comment_count,
                    'like_count': like_count,
                    'site_title': site_blog_info.title,
                    'domaine': site.domaine,
                    'site_id': site_id,
                    'user_info': user_info,
                    'user_add': user_add,
                    'user_count': user_count,
                    'unread_notifications_count': unread_notifications_count,
                    'notifications': notifications,
                    'user_standards': user_standards,
                    'likes_count': likes_count,
                }
                return render(request, 'dashboard_blog.html', context)
            else:
                return HttpResponse("No site information found.")
        else:
            return HttpResponse("No site found for the user.")

#######################################################################################################
# fonction pou ale sou menu an
########################################################################################################

def menu(request, domaine):
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
                site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
                # Récupérez les informations de l'utilisateur à partir du modèle User_Main
                user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
                site_id = site_blog_info.id

                # Récupérer les catégories et les tags
                categories = Category_Blog.objects.all()
                tags = Tag_Blog.objects.all()

                # Récupérer les articles de blog associés au site blog, triés par date de création
                posts = Post_Blog.objects.filter(site=site_blog_info).order_by('-created_at')


                # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
                context = {
                    'user_info': user_info,
                    'site_id': site_id,
                    'site_title': site_blog_info.title,
                    'categories': categories,  # Ajoutez les catégories au contexte
                    'tags': tags,  # Ajoutez les tags au contexte
                    'posts': posts,
                    'domaine': site.domaine,
                    'user_grade': user.grade,
                }
                # Logique de vue pour afficher les messages
                return render(request, 'menu.html', context)
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
            site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
            # Récupérez les informations de l'utilisateur à partir du modèle User_Main
            user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
            site_id = site_blog_info.id

            # Récupérer les catégories et les tags
            categories = Category_Blog.objects.all()
            tags = Tag_Blog.objects.all()

            # Récupérer les articles de blog associés au site blog, triés par date de création
            posts = Post_Blog.objects.filter(site=site_blog_info).order_by('-created_at')


            # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
            context = {
                'user_info': user_info,
                'site_id': site_id,
                'site_title': site_blog_info.title,
                'categories': categories,  # Ajoutez les catégories au contexte
                'tags': tags,  # Ajoutez les tags au contexte
                'posts': posts,
                'domaine': site.domaine,
            }
            # Logique de vue pour afficher les messages
            return render(request, 'menu.html', context)
        else:
            # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
            return HttpResponse("No site found for the user.")

#######################################################################################################
# fonction pou ale sou theme la
########################################################################################################

def marketplace(request, domaine):
    # Obtenez l'utilisateur connecté
    user = request.user
    if user.grade == '2':
        creator = user.created_by
        if creator:
            # Récupérer les informations du site lié à l'utilisateur connecté
            site = Sitewebpam.objects.filter(id_user=user).first()
            # Vérifier si un site a été trouvé pour l'utilisateur
            if site:
                # Récupérez les informations de l'utilisateur à partir du modèle User_Main
                user_info = User_Main.objects.get(username=user.username)
                user_add = Info_utilisateurs.objects.get(id_user=creator)
                site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
                unread_notifications_count = Notification.objects.filter(site=site_blog_info, is_read=False).count()
                notifications = Notification.objects.filter(site=site_blog_info).order_by('-created_at')[:5]
                site_id = site_blog_info.id

                # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
                context = {
                    'user_info': user_info,
                    'user_add' : user_add,
                    'site_title': site_blog_info.title,
                    'site_id': site_id,
                    'unread_notifications_count': unread_notifications_count,
                    'notifications': notifications,
                    'domaine': site.domaine,
                }
                return render(request, 'marketplace.html', context)
            else:
                # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
                return HttpResponse("No site found for the user.")
        else:
            return HttpResponse("No creator found for this user.")
    else:
        # Récupérer les informations du site lié à l'utilisateur connecté
        site = Sitewebpam.objects.filter(id_user=user).first()

        # Vérifier si un site a été trouvé pour l'utilisateur
        if site:

            # Récupérez les informations de l'utilisateur à partir du modèle User_Main
            user_info = User_Main.objects.get(username=user.username)
            user_add = Info_utilisateurs.objects.get(id_user=user)
            site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
            unread_notifications_count = Notification.objects.filter(site=site_blog_info, is_read=False).count()
            notifications = Notification.objects.filter(site=site_blog_info).order_by('-created_at')[:5]
            site_id = site_blog_info.id

            # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
            context = {
                'user_info': user_info,
                'user_add' : user_add,
                'site_title': site_blog_info.title,
                'site_id': site_id,
                'unread_notifications_count': unread_notifications_count,
                'notifications': notifications,
                'domaine': site.domaine,
            }
            return render(request, 'marketplace.html', context)
        else:
            # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
            return HttpResponse("No site found for the user.")

#######################################################################################################
# fonction pou ale sou manage la
########################################################################################################

def manage(request):
    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les informations du site lié à l'utilisateur connecté
    site = Sitewebpam.objects.filter(id_user=user).first()

    # Récupérer les informations spécifiques au site à afficher
    site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
    post_count = Post_Blog.objects.filter(author=site_blog_info.id_Admin_Blog).count()
    comment_count = Comment_Blog.objects.filter(post__author=site_blog_info.id_Admin_Blog).count()
    like_count = Like_Blog.objects.filter(post__author=site_blog_info.id_Admin_Blog).count()
    abonement = Abonement.objects.filter(id_user=user).first()
    user_info = User_Main.objects.get(username=user.username)

    context = {
        'site': site,
        'site_blog_info': site_blog_info,
        'post_count': post_count,
        'comment_count': comment_count,
        'like_count': like_count,
        'abonement': abonement,
        'user_info' : user_info,
    }
    return render(request, 'manage.html', context)

# #############################################################################################################################
# fonctiom pou mete domaine nan url
#############################################################################################################################

def view_site(request, domaine, site_id):

    # categories = Category_Blog.objects.all()

    # Récupérer le site blog correspondant au domaine
    site_blog = get_object_or_404(Site_Blog, id_sitepam__domaine=domaine)

    # Récupérer les articles de blog associés au site blog, triés par date de création
    posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')


    # Initialiser un ensemble vide pour stocker toutes les catégories
    categories = set()
    tags = set()


    for post in posts:
        post_categories = post.categories.all()  # Récupérer toutes les catégories du post
        post_tags = post.tags.all()
        categories.update(post_categories)  # Ajouter les catégories au ensemble
        tags.update(post_tags)


    # Récupérer les titres des posts
    post_titles = [post.title for post in posts]

    # Récupérer les publications mises en avant
    featured_posts = Post_Blog.objects.filter(site=site_blog, is_featured=True)
    featured_posts_titles = [featured_post.title for featured_post in featured_posts]

    # Récupérer les 5 derniers posts du site
    latest_posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')[:5]

    # Vérifier si 'user_standard' existe dans la session
    if 'user_standard' in request.session:
        user_standard = User_Standard.objects.get(id=request.session['user_standard'])
        initials = user_standard.initials
    else:
        user_standard = None
        initials = ''

    # Pagination
    paginator = Paginator(posts, 4)  # 4 articles par page
    page_number = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)  # Afficher la première page si le paramètre de la page n'est pas un entier
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)  # Afficher la dernière page si la page demandée est vide

    # Récupérer la couleur du site à partir de la base de données
    site_color_name = site_blog.Couleur
    color_map = {
        'rouge': '#FF0000',
        'vert': '#00FF00',
        'bleu': '#0000FF',
        'rose': '#FFC0CB',
        'orange': '#FFA500'
    }

    site_color_hex = color_map.get(site_color_name.lower(), '#000000')


    context = {
        'site': site_blog.id_sitepam,
        'featured_posts' : featured_posts,
        'site_color': site_color_hex,
        'categories': categories,
        'site_blog': site_blog,
        'domaine': domaine,
        'posts': paginated_posts,
        'latest_posts': latest_posts,
        'site_id': site_blog.id,
        'post_titles': post_titles,
        'featured_posts_titles': featured_posts_titles,
        'tags': tags,
        'user_standard': user_standard,
        'initials': initials,

    }

    # Rendre le modèle HTML avec le contexte
    return render(request, 'site_view.html', context)

# #############################################################################################################################
# fonctiom pou kreye yon post
#############################################################################################################################
def create_post(request, site_id):
    try:
        # Récupérer l'utilisateur connecté
        user = request.user

        if user.grade == '2':
            # Récupérer le créateur (utilisateur de grade 1)
            creator = user.created_by
            if creator:
                # Récupérer le site lié au créateur
                site = Sitewebpam.objects.filter(id_user=creator).first()
                if site:
                    if request.method == 'POST':
                        title = request.POST['title']
                        image = request.FILES['image']
                        content = request.POST['content']
                        selected_categories = request.POST.getlist('categories')
                        tags = request.POST.getlist('tags')

                        # Vérifie si la case à cocher est cochée dans la requête POST
                        is_featured = 0
                        if 'featured' in request.POST:
                            is_featured = 1


                        # Créer le post avec l'admin connecté comme auteur
                        post = Post_Blog.objects.create(
                            title=title,
                            image=image,
                            content=content,
                            author=user,
                            is_featured=is_featured,
                            site_id=site_id
                        )

                        # Associer les catégories sélectionnées au post
                        for category_id in selected_categories:
                            category = Category_Blog.objects.get(pk=category_id)
                            post.categories.add(category)

                        # Associer les tags sélectionnées au post
                        for tag_id in tags:
                            tag = Tag_Blog.objects.get(pk=tag_id)
                            post.tags.add(tag)

                        # Récupérer les catégories et les tags depuis la base de données
                        categories = Category_Blog.objects.all()
                        tags = Tag_Blog.objects.all()

                        # Ajouter les catégories et les tags au contexte
                        context = {
                            'categories': categories,
                            'tags': tags,
                        }

                        # Rediriger après la création
                        return redirect('dashboard_blog', {'domaine': site.domaine})
                    else:
                        # Si la méthode de requête n'est pas POST, renvoyer simplement le formulaire avec les catégories et les tags
                        categories = Category_Blog.objects.all()
                        tags = Tag_Blog.objects.all()
                        return render(request, 'menu.html', {'categories': categories, 'tags': tags})
                else:
                    # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
                    return HttpResponse("No site found for the user.")
            else:
                # Gérer le cas où le créateur n'est pas trouvé
                return HttpResponse("No creator found for this user.")
        else:
            # Récupérer le site lié à l'utilisateur connecté
            site = Sitewebpam.objects.filter(id_user=user).first()

            if site:

                if request.method == 'POST':
                    title = request.POST['title']
                    image = request.FILES['image']
                    content = request.POST['content']
                    selected_categories = request.POST.getlist('categories')
                    tags = request.POST.getlist('tags')

                    # Vérifie si la case à cocher est cochée dans la requête POST
                    is_featured = 0
                    if 'featured' in request.POST:
                        is_featured = 1


                    # Créer le post avec l'admin connecté comme auteur
                    post = Post_Blog.objects.create(
                        title=title,
                        image=image,
                        content=content,
                        author=user,
                        is_featured=is_featured,
                        site_id=site_id
                    )

                    # Associer les catégories sélectionnées au post
                    for category_id in selected_categories:
                        category = Category_Blog.objects.get(pk=category_id)
                        post.categories.add(category)

                    # Associer les tags sélectionnées au post
                    for tag_id in tags:
                        tag = Tag_Blog.objects.get(pk=tag_id)
                        post.tags.add(tag)

                    # Récupérer les catégories et les tags depuis la base de données
                    categories = Category_Blog.objects.all()
                    tags = Tag_Blog.objects.all()

                    # Ajouter les catégories et les tags au contexte
                    context = {
                        'categories': categories,
                        'tags': tags,
                    }

                    # Rediriger après la création
                    return redirect('dashboard_blog', {'domaine': site.domaine})
                else:
                    # Si la méthode de requête n'est pas POST, renvoyer simplement le formulaire avec les catégories et les tags
                    categories = Category_Blog.objects.all()
                    tags = Tag_Blog.objects.all()
                    return render(request, 'menu.html', {'categories': categories, 'tags': tags})
            else:
                # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
                return HttpResponse("No site found for the user.")

    except Exception as e:
        error_message = str(e)
        return redirect(reverse('dashboard_blog') + f'?message={error_message}')

############################################################################################################################
# fonction pou kreye categories
###############################################################################################################################
def create_category(request, site_id):
    # Récupérer l'utilisateur connecté
    user = request.user

    if user.grade == '2':
        # Récupérer le créateur (utilisateur de grade 1)
        creator = user.created_by
        if creator:
            # Récupérer les informations du site lié à l'utilisateur connecté
            sitewebpam = Sitewebpam.objects.filter(id_user=creator).first()
            if request.method == "POST":
                # Récupérer les données du formulaire
                name = request.POST.get('name')
                description = request.POST.get('description')

                # Récupérer le site correspondant
                site = Site_Blog.objects.get(id=site_id)

                # Créer la catégorie
                category = Category_Blog.objects.create(name=name, description=description)

                # Ajouter la catégorie au site
                site.categories.add(category)

            # Rediriger vers une autre page ou retourner une réponse
            return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})  # Redirection vers le tableau de bord par example
        else:
            # Gérer le cas où le créateur n'est pas trouvé
            return HttpResponse("No creator found for this user.")
    else:
        # Récupérer les informations du site lié à l'utilisateur connecté
        sitewebpam = Sitewebpam.objects.filter(id_user=user).first()
        if request.method == "POST":
            # Récupérer les données du formulaire
            name = request.POST.get('name')
            description = request.POST.get('description')

            # Récupérer le site correspondant
            site = Site_Blog.objects.get(id=site_id)

            # Créer la catégorie
            category = Category_Blog.objects.create(name=name, description=description)

            # Ajouter la catégorie au site
            site.categories.add(category)

            # Rediriger vers une autre page ou retourner une réponse
            return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})  # Redirection vers le tableau de bord par example

        return render(request, 'menu.html', {'site_id': site_id})

############################################################################################################################
# fonction pou kreye tags
###############################################################################################################################
def create_tag(request, site_id):
    # Récupérer l'utilisateur connecté
    user = request.user
    if user.grade == '2':
        # Récupérer le créateur (utilisateur de grade 1)
        creator = user.created_by
        if creator:
            # Récupérer les informations du site lié à l'utilisateur connecté
            sitewebpam = Sitewebpam.objects.filter(id_user=creator).first()
            if request.method == "POST":
                # Récupérer les données du formulaire
                name = request.POST.get('name')

                # Récupérer le site correspondant
                site = Site_Blog.objects.get(id=site_id)

                # Créer le tag
                tag = Tag_Blog.objects.create(name=name)

                # Ajouter le tag au site
                site.tags.add(tag)

                # Rediriger vers une autre page ou retourner une réponse
                return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})  # Redirection vers le tableau de bord par exemple
            
            return render(request, 'menu.html', {'site_id': site_id})
        else:
            # Gérer le cas où le créateur n'est pas trouvé
            return HttpResponse("No creator found for this user.")
    else:
        sitewebpam = Sitewebpam.objects.filter(id_user=user).first()
        if request.method == "POST":
            # Récupérer les données du formulaire
            name = request.POST.get('name')

            # Récupérer le site correspondant
            site = Site_Blog.objects.get(id=site_id)

            # Créer le tag
            tag = Tag_Blog.objects.create(name=name)

            # Ajouter le tag au site
            site.tags.add(tag)

            # Rediriger vers une autre page ou retourner une réponse
            return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})  # Redirection vers le tableau de bord par exemple

        return render(request, 'menu.html', {'site_id': site_id})

##########################################################################################################
# fonction pou itilizatè standa kreye kont
##########################################################################################################

def register_blog(request, domaine, site_id):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        # Récupérer la première lettre du nom et du prénom
        first_letter_firstname = firstname[0].upper() if firstname else ''
        first_letter_lastname = lastname[0].upper() if lastname else ''

        initials = ''

        if firstname:
            initials += first_letter_firstname
        if lastname:
            initials += first_letter_lastname

        # Vérifications des données du formulaire
        if not all([firstname, lastname, username, email, password, confirmpassword]):
            messages.error(request, "Veuillez remplir tous les champs du formulaire.")
            return render(request, 'signup_blog.html')

        if password != confirmpassword:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'signup_blog.html')

        if User_Standard.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà utilisé.")
            return render(request, 'signup_blog.html')

        if User_Standard.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà associé à un compte.")
            return render(request, 'signup_blog.html')
        


        # Enregistrement de l'utilisateur
        user_standard = User_Standard.objects.create(
            nom=lastname,
            prenom=firstname,
            username=username,
            email=email,
            password=make_password(password),
            initials=initials,
            site_id=site_id,
        )
        user_standard.save()



        return render(request, 'signin_blog.html', {'site_id': site_id, 'domaine': domaine})

    return render(request, 'signup_blog.html', {'site_id': site_id, 'domaine': domaine})

##########################################################################################################
# fonction pou itilizatè standa a konekte sou sit itilizatè prensipal yo
##########################################################################################################

def signin_blog(request, domaine, site_id):
    if request.method == "POST":
        username = request.POST.get('username')  # Récupérez le nom d'utilisateur depuis le formulaire
        password = request.POST.get('password')

        # Recherchez l'utilisateur dans la table User_Standard par nom d'utilisateur
        try:
            user_standard = User_Standard.objects.get(username=username)
        except User_Standard.DoesNotExist:
            user_standard = None

        # Vérifiez si l'utilisateur existe et si le mot de passe est correct
        if user_standard is not None and user_standard.check_password(password):
            # Authentifiez l'utilisateur avec le backend d'authentification par défaut
            user_authenticated = authenticate(request, username=user_standard.username, password=password)
            if user_authenticated is not None:
                # Vérifiez si l'utilisateur est associé au site en question
                if user_standard.site_id == int(site_id):
                    # Connectez l'utilisateur
                    login(request, user_authenticated, backend='blog.backends.UserStandardBackend')
                    # Stocker l'ID de l'utilisateur dans la session
                    request.session['user_standard'] = user_standard.id
                    return redirect('view_site', domaine=domaine, site_id=site_id)
                else:
                    return HttpResponse("No user found sorry")
            else:
                return HttpResponse("Failed to login")
        else:
            return HttpResponse("Failed to login")

    return render(request, 'signin_blog.html', {'site_id': site_id, 'domaine': domaine})

##########################################################################################################
# fonction pou itilizatè standa dekonekte nan kont li an
##########################################################################################################

def logout_blog(request, domaine, site_id):
    logout(request)
    # Supprimer la session 'user_standard'
    if 'user_standard' in request.session:
        del request.session['user_standard']
    return redirect('view_site', domaine=domaine, site_id=site_id)

##########################################################################################################
# fonction pou wè plis detay nan pòs yo
##########################################################################################################

def post_detail(request, domaine, post_title, site_id, post_id):
    # Récupérer les informations du site lié à l'utilisateur connecté
    site_blog = Site_Blog.objects.get(id=site_id)
    latest_posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')
    post = get_object_or_404(Post_Blog, pk=post_id)
    # Récupérer la catégorie du post
    categories = post.categories.all()

    # Récupérer les tags associés à ce post
    tags = post.tags.all()

    site_color_name = site_blog.Couleur
    color_map = {
        'rouge': '#FF0000',
        'vert': '#00FF00',
        'bleu': '#0000FF',
        'rose': '#FFC0CB',
        'orange': '#FFA500'
    }
    site_color_hex = color_map.get(site_color_name.lower(), '#000000')
    # Récupérer les commentaires associés au post
    comments = Comment_Blog.objects.filter(post=post)

    # Récupérer l'ID de l'utilisateur à partir de la session avec la clé 'user_standard'
    user_standard_id = request.session.get('user_standard')
    if user_standard_id:
        # Récupérer l'utilisateur standard correspondant
        user_standard = get_object_or_404(User_Standard, pk=user_standard_id)
        # Obtenir les initiales de l'utilisateur
        initials = user_standard.initials
        return render(request, 'post_detail.html', {'domaine': domaine, 'site_blog': site_blog, 'post': post, 'tags': tags, 'categories': categories, 'site_color': site_color_hex, 'site_id': site_blog.id, 'latest_posts': latest_posts, 'user_standard': user_standard, 'comments': comments, 'initials': initials, 'post_titles': post_title})
    else:
        user_standard = None

    return render(request, 'post_detail.html', {'domaine': domaine, 'site_blog': site_blog, 'post': post, 'tags': tags, 'categories': categories, 'site_color': site_color_hex, 'site_id': site_blog.id, 'latest_posts': latest_posts, 'user_standard': user_standard, 'comments': comments, 'post_titles': post_title})

##########################################################################################################
# fonction pou itilizatè standa a kapab fè yon kòmantè
##########################################################################################################

def submit_comment(request, domaine, post_title, site_id, post_id):
    user_standard = None  # Initialiser user_standard à None
    if request.method == 'POST':
        user_standard_id = request.session.get('user_standard')
        site_blog = Site_Blog.objects.get(id=site_id)
        latest_posts = Post_Blog.objects.filter(site=site_blog).order_by('-created_at')
        post = get_object_or_404(Post_Blog, pk=post_id)
        categories = Category_Blog.objects.all()
        tags = Tag_Blog.objects.all()
        site_color_name = site_blog.Couleur
        color_map = {
            'rouge': '#FF0000',
            'vert': '#00FF00',
            'bleu': '#0000FF',
            'rose': '#FFC0CB',
            'orange': '#FFA500'
        }
        site_color_hex = color_map.get(site_color_name.lower(), '#000000')
        comments = Comment_Blog.objects.filter(post=post)
        content = request.POST.get('comment_content')

        if user_standard_id:
            user_standard = get_object_or_404(User_Standard, pk=user_standard_id)
            comment = Comment_Blog.objects.create(post=post, author=user_standard, content=content)
            comment.save()
            # Créer une notification pour le créateur du post
            Notification.objects.create(
                site=post.site,  # Assurez-vous que le modèle Post_Blog a un champ `author`
                message=f'{user_standard.username} commented on your post.',
                user=user_standard,
            )

        return render(request, 'post_detail.html', {
            'domaine': domaine,
            'site_blog': site_blog,
            'post': post,
            'tags': tags,
            'categories': categories,
            'site_color': site_color_hex,
            'site_id': site_blog.id,
            'latest_posts': latest_posts,
            'user_standard': user_standard,
            'comments': comments,
            'post_titles': post_title
        })
    else:
        return render(request, 'post_detail.html', {
            'domaine': domaine,
            'site_blog': site_blog,
            'post': post,
            'tags': tags,
            'categories': categories,
            'site_color': site_color_hex,
            'site_id': site_blog.id,
            'latest_posts': latest_posts,
            'user_standard': user_standard,  # Assurez-vous que user_standard est passé, même s'il est None
            'comments': comments,
            'post_titles': post_title
        })

##########################################################################################################
# fonction pou download resous nan yon lòt template
##########################################################################################################

class DownloadResourcesView(View):
    def download_resource(self, url, folder):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Obtenir le nom du fichier ou du répertoire à partir de l'URL
            filename = os.path.join(folder, os.path.basename(url.rstrip('/')))
            # Créer le dossier parent s'il n'existe pas déjà
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            # Si l'URL se termine par '/', il s'agit d'un répertoire
            if url.endswith('/'):
                # Créer le répertoire
                os.makedirs(filename, exist_ok=True)
            else:
                # Écrire le fichier
                with open(filename, 'wb') as f:
                    response.raw.decode_content = True
                    f.write(response.content)
            print(f"Resource téléchargée : {url}")

    def download_html(self, url, folder):
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(folder, "index.html")  # Nommez le fichier HTML index.html
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"HTML téléchargé : {url}")

            # Remplacer le contenu du fichier site_view.html avec le contenu téléchargé
            with open(os.path.join(settings.BASE_DIR, 'blog', 'templates', 'site_view.html'), 'wb') as f:
                f.write(response.content)

    def get(self, request):
        url = request.GET.get('url')
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                # Créer un dossier pour sauvegarder les ressources
                folder = "ressources"
                os.makedirs(folder, exist_ok=True)

                # Télécharger le contenu HTML de la page principale
                self.download_html(url, folder)

                # Afficher un popup informant que le template est disponible
                return JsonResponse({'message': 'Le template est disponible.'})

        return HttpResponse('URL invalide ou impossible de télécharger les ressources', status=400)

##########################################################################################################
# fonction pou test pou paypal la
##########################################################################################################

def pricing(request):
    plans = Plan.objects.all()
    context = {'plans' : plans}
    return render(request, "pricing.html", context)

##########################################################################################################
# fonction pou voye nan paj pou modifye pòs la ak kèk lòt agiman
##########################################################################################################

def edit_post(request, post_id):
    # Récupérer l'utilisateur connecté
    user = request.user

    if user.grade == '2':
        # Récupérer le créateur (utilisateur de grade 1)
        creator = user.created_by
        if creator:
            # Récupérer les informations du site lié à l'utilisateur connecté
            site = Sitewebpam.objects.filter(id_user=creator).first()
            if site:

                user_info = User_Main.objects.get(username=user.username)
                user_add = Info_utilisateurs.objects.get(id_user=creator)
                # Récupérer le post à éditer
                post = Post_Blog.objects.get(pk=post_id)
                categories = Category_Blog.objects.all()
                tags = Tag_Blog.objects.all()

                # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
                context = {
                    'user_info': user_info,
                    'user_add': user_add,
                    'post': post,
                    'categories': categories,
                    'tags': tags,
                    'domaine': site.domaine,
                }
                return render(request, 'edit_post.html', context)
            else:
                # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
                return HttpResponse("No site found for the user.")
        else:
            # Gérer le cas où le créateur n'est pas trouvé
            return HttpResponse("No creator found for this user.")
    else:

        # Récupérer les informations du site lié à l'utilisateur connecté
        site = Sitewebpam.objects.filter(id_user=user).first()

        if site:

            user_info = User_Main.objects.get(username=user.username)
            user_add = Info_utilisateurs.objects.get(id_user=user)
            # Récupérer le post à éditer
            post = Post_Blog.objects.get(pk=post_id)
            categories = Category_Blog.objects.all()
            tags = Tag_Blog.objects.all()

            # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
            context = {
                'user_info': user_info,
                'user_add': user_add,
                'post': post,
                'categories': categories,
                'tags': tags,
                'domaine': site.domaine,
            }
            return render(request, 'edit_post.html', context)
        else:
            # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
            return HttpResponse("No site found for the user.")

##########################################################################################################
# fonction pou modifye yon pòs en fonksyon de id pòs la
##########################################################################################################

def edit_post_logic(request, post_id):
    try:

        # Récupérer l'utilisateur connecté
        user = request.user

        # Récupérer le post à éditer
        post = Post_Blog.objects.get(pk=post_id)

        if user.grade == '2':
            # Récupérer le créateur (utilisateur de grade 1)
            creator = user.created_by
            if creator:
                # Récupérer les informations du site lié à l'utilisateur connecté
                sitewebpam = Sitewebpam.objects.filter(id_user=creator).first()
                if request.method == 'POST':
                    # Récupérer les données du formulaire POST
                    title = request.POST['title']
                    image = request.FILES.get('image', None)
                    content = request.POST['content']
                    selected_categories = request.POST.getlist('categories')
                    tags = request.POST.getlist('tags')

                    # Récupérer la valeur du champ "featured" de la requête POST
                    is_featured = request.POST.get('featured', False) == 'on'

                    # Mettre à jour les champs du post avec les nouvelles données
                    post.title = title
                    if image:
                        post.image = image
                    post.content = content
                    post.is_featured = is_featured

                    # Supprimer toutes les catégories associées au post
                    post.categories.clear()
                    # Ajouter les catégories sélectionnées au post
                    for category_id in selected_categories:
                        category = Category_Blog.objects.get(pk=category_id)
                        post.categories.add(category)
                    # Enregistrer les modifications du post
                    post.save()

                    # Rediriger après l'édition
                    return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})
                else:
                    # Si la méthode de requête n'est pas POST, pré-remplir le formulaire avec les données du post
                    categories = Category_Blog.objects.all()
                    tags = Tag_Blog.objects.all()
                    context = {
                        'post': post,
                        'categories': categories,
                        'tags': tags,
                    }
                    return render(request, 'edit_post.html', context)

            else:
                # Gérer le cas où le créateur n'est pas trouvé
                return HttpResponse("No creator found for this user.")
        else:
            # Récupérer les informations du site lié à l'utilisateur connecté
            sitewebpam = Sitewebpam.objects.filter(id_user=user).first()
        

            if request.method == 'POST':
                # Récupérer les données du formulaire POST
                title = request.POST['title']
                image = request.FILES.get('image', None)
                content = request.POST['content']
                selected_categories = request.POST.getlist('categories')
                tags = request.POST.getlist('tags')

                # Récupérer la valeur du champ "featured" de la requête POST
                is_featured = request.POST.get('featured', False) == 'on'

                # Mettre à jour les champs du post avec les nouvelles données
                post.title = title
                if image:
                    post.image = image
                post.content = content
                post.is_featured = is_featured

                # Supprimer toutes les catégories associées au post
                post.categories.clear()
                # Ajouter les catégories sélectionnées au post
                for category_id in selected_categories:
                    category = Category_Blog.objects.get(pk=category_id)
                    post.categories.add(category)
                # Enregistrer les modifications du post
                post.save()

                # Rediriger après l'édition
                return redirect('dashboard_blog', {'domaine': sitewebpam.domaine})
            else:
                # Si la méthode de requête n'est pas POST, pré-remplir le formulaire avec les données du post
                categories = Category_Blog.objects.all()
                tags = Tag_Blog.objects.all()
                context = {
                    'post': post,
                    'categories': categories,
                    'tags': tags,
                }
                return render(request, 'edit_post.html', context)

    except Post_Blog.DoesNotExist:
        # Gérer le cas où le post avec l'ID donné n'existe pas
        return HttpResponse("Post does not exist")

##########################################################################################################
# fonction pou siprime yon pòs
##########################################################################################################

def delete_post(request, post_id):
    try:

        user = request.user
        if user.grade == '2':
            # Récupérer le créateur (utilisateur de grade 1)
            creator = user.created_by
            if creator:
                sitewebpam_type = Sitewebpam.objects.get(id_user=creator)
                domaine = sitewebpam_type.domaine
                post = get_object_or_404(Post_Blog, pk=post_id)
                post.delete()
                return redirect('dashboard_blog', domaine=domaine)
            else:
                # Gérer le cas où le créateur n'est pas trouvé
                return HttpResponse("No creator found for this user.")
        else:
            sitewebpam_type = Sitewebpam.objects.get(id_user=user)
            domaine = sitewebpam_type.domaine
            post = get_object_or_404(Post_Blog, pk=post_id)
            post.delete()
            return redirect('dashboard_blog', domaine=domaine)
        
    except Post_Blog.DoesNotExist:
        # Gérer le cas où le post avec l'ID donné n'existe pas
        return HttpResponse("Post does not exist")

##########################################################################################################
# fonction pou itilizatè standa yo bay yon like
##########################################################################################################

def like_post(request, post_id):
    user_standard_id = request.session.get('user_standard')
    if user_standard_id:
        user_standard = get_object_or_404(User_Standard, pk=user_standard_id)
        post = get_object_or_404(Post_Blog, id=post_id)
        if not Like_Blog.objects.filter(post=post, user=user_standard).exists():
            like = Like_Blog.objects.create(post=post, user=user_standard)
            like.save()
            # Créer une notification pour le créateur du post
            Notification.objects.create(
                site=post.site,
                message=f'{user_standard.username} liked your post.',
                user=user_standard,
            )
            return JsonResponse({'message': 'Post liked successfully', 'post_id': post_id})
        else:
            return JsonResponse({'message': 'You already liked this post', 'post_id': post_id})
    else:
        return JsonResponse({'message': 'Authentication required', 'post_id': post_id})

##########################################################################################################
# fonction pou itilizatè standa yo retire yon like ke yo t bay
##########################################################################################################

def remove_like(request, post_id):
    # Récupérer l'utilisateur actuellement connecté (s'il y en a un)
    user_standard_id = request.session.get('user_standard')
    if user_standard_id:
        user_standard = get_object_or_404(User_Standard, pk=user_standard_id)
        post = get_object_or_404(Post_Blog, id=post_id)
        # Vérifier si un like existe pour ce post et cet utilisateur
        like = Like_Blog.objects.filter(post=post, user=user_standard).first()
        if like:
            like.delete()  # Supprimer le like de la base de données
            return JsonResponse({'message': 'Like removed successfully', 'post_id': post_id})
        else:
            return JsonResponse({'message': 'User not authenticated', 'post_id': post_id})
    else:
        return JsonResponse({'message': 'User not authenticated', 'post_id': post_id})

##########################################################################################################
# fonction pou itilizatè standa yo fè yon rechèch nan sit lan
##########################################################################################################

def search_post_in_site(request, domaine, site_id):
    # Récupérer le terme de recherche à partir de la requête GET
    search_term = request.GET.get('search_term')

    # Récupérer le site spécifié dans la requête
    site_blog = get_object_or_404(Site_Blog, id=site_id)

    site_color_name = site_blog.Couleur
    color_map = {
        'rouge': '#FF0000',
        'vert': '#00FF00',
        'bleu': '#0000FF',
        'rose': '#FFC0CB',
        'orange': '#FFA500'
    }
    site_color_hex = color_map.get(site_color_name.lower(), '#000000')

    # Récupérer tous les posts associés à ce site
    posts = Post_Blog.objects.filter(site=site_blog)

    # Si un terme de recherche est fourni, filtrer les posts en fonction de ce terme
    if search_term:
        posts = posts.filter(
            Q(title__icontains=search_term) |
            Q(categories__name__icontains=search_term) |
            Q(tags__name__icontains=search_term)
        ).distinct()

    # Récupérer les catégories associées aux posts filtrés
    categories = Category_Blog.objects.filter(post_blog__in=posts).distinct()
    # Récupérer tous les tags associés à ce site
    tags = Tag_Blog.objects.filter(post_blog__in=posts).distinct()

    # Passer les résultats de la recherche au template pour affichage
    context = {
        'site_blog': site_blog,
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'search_term': search_term,
        'domaine': domaine,
        'site_color': site_color_hex,
        'site_id': site_blog.id,
    }

    return render(request, 'site_view.html', context)

##########################################################################################################
# fonction pou afiche Category yo lèw klike sou yo
##########################################################################################################

def category_posts(request, domaine, site_id, category_id):
    # Récupérer la catégorie spécifiée
    category = get_object_or_404(Category_Blog, id=category_id)

    # Récupérer le site spécifié dans la requête
    site_blog = get_object_or_404(Site_Blog, id=site_id)

    site_color_name = site_blog.Couleur
    color_map = {
        'rouge': '#FF0000',
        'vert': '#00FF00',
        'bleu': '#0000FF',
        'rose': '#FFC0CB',
        'orange': '#FFA500'
    }
    site_color_hex = color_map.get(site_color_name.lower(), '#000000')

    # Récupérer tous les posts associés à cette catégorie
    posts = Post_Blog.objects.filter(categories=category)

    # Passer les résultats au template pour affichage
    context = {
        'category': category,
        'site_blog': site_blog,
        'posts': posts,
        'domaine': domaine,
        'site_color': site_color_hex,
        'site_id': site_blog.id,
    }

    return render(request, 'site_view.html', context)

##########################################################################################################
# fonction pou ale nan paj create_admin nan ak kèk lòt agiman
##########################################################################################################

def create_admin(request, domaine):

    # Récupérer l'utilisateur connecté
    user = request.user

    # Récupérer les informations du site lié à l'utilisateur connecté
    site = Sitewebpam.objects.filter(id_user=user).first()

    # Vérifier si un site a été trouvé pour l'utilisateur
    if site:
        # Récupérer les informations spécifiques au site à afficher
        site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
        # Récupérez les informations de l'utilisateur à partir du modèle User_Main
        user_info = User_Main.objects.get(username=user.username)  # Changer pour correspondre à la façon dont vous identifiez un utilisateur
        site_id = site_blog_info.id


        # Créez un dictionnaire contenant les informations de l'utilisateur pour les passer au modèle HTML
        context = {
            'user_info': user_info,
            'site_id': site_id,
            'site_title': site_blog_info.title,
            'domaine': site.domaine,
        }
        return render(request, 'create_admin.html', context)
    else:
        # Gérer le cas où aucun site n'est trouvé pour l'utilisateur
        return HttpResponse("No site found for the user.")

##########################################################################################################
# fonction pou itilizatè prensipal yo kreye yon admin
##########################################################################################################

def create_admin_logic(request, domaine, site_id):
    user = request.user

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User_Main.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken, please try another.')
            return render(request, 'create_admin.html', {'domaine': domaine, 'site_id': site_id})

        if User_Main.objects.filter(email=email).exists():
            messages.error(request, 'This email is already associated with an account.')
            return render(request, 'create_admin.html', {'domaine': domaine, 'site_id': site_id})

        if not username.isalnum():
            messages.error(request, 'Username must be alphanumeric.')
            return render(request, 'create_admin.html', {'domaine': domaine, 'site_id': site_id})

        if password != confirm_password:
            messages.error(request, 'The passwords did not match!')
            return render(request, 'create_admin.html', {'domaine': domaine, 'site_id': site_id})

        # Convertir la date de naissance au format YYYY-MM-DD
        try:
            date_of_birth = datetime.strptime(date_of_birth, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Date format is invalid. Please use DD/MM/YYYY.')
            return render(request, 'create_admin.html', {'domaine': domaine, 'site_id': site_id})

        sitewebpam = Sitewebpam.objects.filter(id_user=user).first()

        try:
            site = Site_Blog.objects.get(id=site_id)
        except Site_Blog.DoesNotExist:
            messages.error(request, 'Site not found.')
            return render(request, 'create_admin.html', {'domaine': domaine, 'site_id': site_id})

        create_admin = User_Main.objects.create(
            nom=last_name,
            prenom=first_name,
            username=username,
            email=email,
            password=make_password(password),
            portable=phone_number,
            date_de_nais=date_of_birth,
            grade="2",
            is_active=True,
            created_by=user  # Définit l'utilisateur actuel comme créateur
        )
        create_admin.save()

        return redirect('dashboard_blog', domaine=sitewebpam.domaine)

    return render(request, 'create_admin.html', {'domaine': domaine, 'site_id': site_id})

##########################################################################################################
# fonction pou itilizatè prensipal yo modifye header sit yo a
##########################################################################################################

def design_header_site_blog(request, domaine, site_id):
    user = request.user
    site = Sitewebpam.objects.filter(id_user=user).first()
    if site:
        site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
        if site_blog_info:
            user_info = User_Main.objects.get(username=user.username)
            user_add = Info_utilisateurs.objects.get(id_user=user)
            unread_notifications_count = Notification.objects.filter(site=site_blog_info, is_read=False).count()
            notifications = Notification.objects.filter(site=site_blog_info).order_by('-created_at')[:5]
            context = {
                'site_title': site_blog_info.title,
                'domaine': site.domaine,
                'site_id': site_id,
                'user_info': user_info,
                'user_add': user_add,
                'unread_notifications_count': unread_notifications_count,
                'notifications': notifications,
            }
            return render(request, 'customize_header.html', context)
        else:
            return HttpResponse("No site information found.")
    else:
        return HttpResponse("No site found for the user.")



def capture_navbar_data(request):
    if request.method == 'POST':
        try:
            # Récupérer les données JSON depuis la requête POST
            navbar_data = json.loads(request.body)
            print('Données JSON reçues :', navbar_data)

            # Stocker les données JSON en session ou dans la base de données
            request.session['navbar_data'] = navbar_data

            # Répondre avec un succès et une redirection
            return JsonResponse({'status': 'success', 'redirect_url': '/display_navbar_data/'})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Erreur de décodage JSON'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


def display_navbar_data(request, domaine, site_id):
    return render(request, 'display_navbar_data.html')



# def save_navbar_html(request):
#     if request.method == 'POST':
#         # Récupérer les données POST envoyées depuis le frontend
#         site_id = request.POST.get('site_id')  # Récupérer l'ID du site
#         navbar_html = request.POST.get('navbar_html')  # Récupérer le HTML de la navbar

#         try:
#             # Utiliser BeautifulSoup pour parser le HTML
#             soup = BeautifulSoup(navbar_html, 'html.parser')
#             navbar_element = soup.find(id='navbar1')  # Trouver l'élément navbar avec l'ID 'navbar1'

#             # Extraire les styles et attributs spécifiques de la navbar
#             navbar_bg = navbar_element.get('class', [])[1]  # Exemple d'extraction de la classe personnalisée pour le fond
#             navbar_font = navbar_element.find('a', class_='navbar-brand').get('style', 'color')  # Exemple pour la couleur de la police du titre
#             navbar_font_size = navbar_element.find('form', class_='form-inline').get('style', 'font-size')  # Exemple pour la taille de la police de la barre de recherche

#             # Extraction des couleurs des liens
#             link_colors = [li.find('a').get('style', 'color') for li in navbar_element.find_all('li', class_='nav-item')]

#             # Vérifier si le site existe
#             try:
#                 site_choice = SiteChoice.objects.get(site_id=site_id)
#             except SiteChoice.DoesNotExist:
#                 site_choice = SiteChoice(site_id=site_id)  # Créer un nouvel objet si inexistant

#             # Mettre à jour les champs du modèle SiteChoice avec les données extraites
#             site_choice.navbar_bg = navbar_bg
#             site_choice.navbar_font = navbar_font
#             site_choice.navbar_font_size = navbar_font_size
#             site_choice.navbar_brand = navbar_element.find('a', class_='navbar-brand').get('style', 'color')
#             site_choice.navbar_link_1 = link_colors[0] if len(link_colors) > 0 else 'default_color'
#             site_choice.navbar_link_2 = link_colors[1] if len(link_colors) > 1 else 'default_color'
#             site_choice.navbar_link_3 = link_colors[2] if len(link_colors) > 2 else 'default_color'
#             site_choice.navbar_link_4 = link_colors[3] if len(link_colors) > 3 else 'default_color'

#             # Sauvegarder les modifications dans la base de données
#             site_choice.save()

#             # Répondre avec une réponse JSON indiquant le succès
#             return JsonResponse({'status': 'success'})

#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
    
#     else:
#         # Répondre avec une erreur si la requête n'est pas de type POST
#         return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})





def extract_color_from_style(style):
    match = re.search(r'color:\s*(.*?);', style)
    if match:
        return match.group(1).strip()
    return ''

def extract_background_color_from_style(style):
    match = re.search(r'background-color:\s*(.*?);', style)
    if match:
        return match.group(1).strip()
    return ''

def extract_font_size_from_style(style):
    match = re.search(r'font-size:\s*(.*?);', style)
    if match:
        return match.group(1).strip()
    return '16px'  # Valeur par défaut si la taille de la police n'est pas spécifiée

def extract_font_family_from_style(style):
    match = re.search(r'font-family:\s*(.*?);', style)
    if match:
        return match.group(1).strip()
    return ''  # Valeur par défaut si la famille de la police n'est pas spécifiée

def save_navbar_html(request, domaine, site_id):
    user = request.user
    site = Sitewebpam.objects.filter(id_user=user).first()
    if site:
        site_blog_info = Site_Blog.objects.filter(id_sitepam=site).first()
        if site_blog_info:
            if request.method == 'POST':
                navbar_html = request.POST.get('navbar_html')

                if not site_id or not navbar_html:
                    return JsonResponse({'status': 'error', 'message': 'Missing required parameters'})

                try:
                    soup = BeautifulSoup(navbar_html, 'html.parser')
                    navbar_element1 = soup.find(id='navbar1')
                    navbar_element2 = soup.find(id='navbar2')
                    navbar_element = navbar_element1 if navbar_element1 else navbar_element2

                    if not navbar_element:
                        return JsonResponse({'status': 'error', 'message': 'Navbar element not found'})

                    navbar_bg_style = navbar_element.get('style', '')
                    navbar_bg_color = extract_background_color_from_style(navbar_bg_style)
                    
                    navbar_font_style = navbar_element.find('a', class_='nav-link').get('style', '')
                    navbar_font_family = extract_font_family_from_style(navbar_font_style)
                    navbar_font_size = extract_font_size_from_style(navbar_font_style)

                    navbar_brand_element = navbar_element.find('a', class_='navbar-brand')
                    if navbar_brand_element:
                        navbar_brand = navbar_brand_element.text.strip()
                        navbar_brand_style = navbar_brand_element.get('style', '')
                        navbar_brand_color = extract_color_from_style(navbar_brand_style)
                    else:
                        navbar_brand = ''
                        navbar_brand_color = ''

                    link_elements = navbar_element.find_all('li', class_='nav-item')
                    link_texts = []
                    link_colors = []
                    link_sizes = []

                    for li in link_elements:
                        a_tag = li.find('a')
                        if a_tag:
                            link_texts.append(a_tag.text.strip())
                            link_style = a_tag.get('style', '')
                            link_color = extract_color_from_style(link_style)
                            link_size = extract_font_size_from_style(link_style)
                            link_colors.append(link_color)
                            link_sizes.append(link_size)

                    site_blog = Site_Blog.objects.get(id=site_id)
                    site_choice, created = SiteChoice.objects.get_or_create(site=site_blog)

                    domaine = site_blog.id_sitepam.domaine

                    site_choice.navbar_bg = navbar_bg_color
                    site_choice.navbar_font = navbar_font_family
                    site_choice.navbar_font_size = navbar_font_size
                    site_choice.navbar_brand = navbar_brand
                    site_choice.navbar_brand_color = navbar_brand_color
                    site_choice.navbar_link_color = link_colors[0] if link_colors else None
                    site_choice.navbar_link_1 = link_texts[0] if len(link_texts) > 0 else None
                    site_choice.navbar_link_2 = link_texts[1] if len(link_texts) > 1 else None
                    site_choice.navbar_link_3 = link_texts[2] if len(link_texts) > 2 else None
                    site_choice.navbar_link_4 = link_texts[3] if len(link_texts) > 3 else None
                    site_choice.navbar_link_size = link_sizes[0] if len(link_sizes) > 0 else None

                    site_choice.save()

                    # Renvoie l'URL de redirection
                    redirect_url = reverse('view_site', args=[domaine, site_id])
                    return JsonResponse({'status': 'success', 'redirect_url': redirect_url})

                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})
            return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})        
        else:
            return HttpResponse("No site information found.")
    else:
        return HttpResponse("No site found for the user.")
