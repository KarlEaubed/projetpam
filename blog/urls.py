from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard, name='dashboardBlog'),
    path('', views.Post_Blog_Create, name='createlog'),
]
