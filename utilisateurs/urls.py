from django.urls import path, include
from utilisateurs import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logOut, name="logout"),
    path('finalize_account/', views.finalize_account, name='finalize_account'),
    path('setup_account', views.setup_account, name="setup_account"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    # path('accounts/', include('allauth.urls')),
]