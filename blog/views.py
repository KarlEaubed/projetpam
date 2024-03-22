from django.shortcuts import render


from .models import Post_Blog, Comment_Blog, Like_Blog, Site_Blog
from .form import Post_Blog_Form

def dashboard(request):
    # pran posts yo
    posts = Post_Blog.objects.all()
    
    # pran total likes yo
    total_likes = Like_Blog.objects.count()
    
    # pran total commentaires yo
    total_comments = Comment_Blog.objects.count()
    
    # Récupérer le nombre total de visiteurs (si vous avez une table pour cela)
    total_visitors = 0  # Remplacez ceci par votre logique de récupération des visiteurs
    
    # session
    # current_site = Site_Blog.objects.get(id=request.user.site_id)
    
    context = {
        'posts': posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_visitors': total_visitors,
        # 'current_site': current_site,
    }
    return render(request, 'dashboard_Blog.html', context)


def Post_Blog_Create(request):
    form = Post_Blog_Form(request.POST or None)
    if form.is_valid():
        form.save
        
    return render(request, 'createblog.html', {'form' : form})


# Create your views here.
