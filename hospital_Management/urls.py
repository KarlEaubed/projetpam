from django.urls import path
from hospital_Management.views import *


urlpatterns = [
    path('create_site_hospital/<int:site_id>', create_site_hospital, name='create_site_hospital'),
    path('dashboard_hospital/<str:domaine>/', dashboard_hospital, name='dashboard_hospital'),
    path('create_admin_hospital/<str:domaine>/', create_admin_hospital, name='create_admin_hospital'),
    path('menu_hospital_doctor/<str:domaine>/', menu_hospital_doctor, name='menu_hospital_doctor'),
    path('create_new_doctor/<str:domaine>/<int:site_id>/', create_new_doctor, name="create_new_doctor"),
    path('menu_hospital_speciality/<str:domaine>/', menu_hospital_speciality, name='menu_hospital_speciality'),
]