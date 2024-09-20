from django.urls import path
from . import views
from portofolio.views import *

urlpatterns = [
    path('create_site_portofolio/<int:site_id>/', create_site_portofolio, name='create_site_portofolio'),
    path('dashboardportoo/<str:domaine>/', dashboardportofolio, name='dashboardportofolio'),
    path('view_site_portofolio/<str:domaine>/', view_site_portofolio, name='view_site_portofolio'),
    path('add_service/<int:site_id>/', add_service, name='add_service'),
    path('modif_service/<int:service_id>/', modif_service, name='modif_service'),
    path('modif_service/<int:service_id>/', views.modif_service, name='modif_service'),
    path('add_info/<int:site_id>/', views.add_info, name='add_info'),
    path('add_about/<int:site_id>/', views.add_about, name='add_about'),
    path('add_pro/<int:site_id>/', views.add_pro, name='add_pro'),
    path('add_hero/<int:site_id>/', views.add_hero, name='add_hero'),
    
    path('send_email/', views.send_email, name='send_email'),
    path('add_carriere/<int:site_id>/',add_carriere, name='add_carriere'),
    path('add_etude/<int:site_id>/',add_etude, name='add_etude'),
    path('add_skill/<int:site_id>/',add_skill, name='add_skill'),
    
    path('send_email/<int:site_id>/', send_email, name='send_email'),
    path('send_whatsapp/<int:site_id>/', send_whatsapp, name='send_whatsapp'),

]
