from django.urls import path, include
from blog.views import *
from hospital_Management.views import *
from utilisateurs import views as utilisateurs_views  # Alias pour les vues de l'application "utilisateurs"
from portofolio.views import *
from school_Management.views import *

urlpatterns = [
    path('', utilisateurs_views.home, name="home"),
    path('signup', utilisateurs_views.signup, name="signup"),
    path('signin', utilisateurs_views.signin, name="signin"),
    path('logout', utilisateurs_views.logOut, name="logout"),
    path('setup_account', utilisateurs_views.setup_account, name="setup_account"),
    path('activate/<uidb64>/<token>', utilisateurs_views.activate, name='activate'),
    path('site_creation/', utilisateurs_views.site_creation, name='site_creation'),
    path('create_site_blog/<int:site_id>/', utilisateurs_views.create_site_blog, name='create_site_blog'),
    path('payment_moncash', utilisateurs_views.payment_moncash, name="payment_moncash"),
    path('checkout/<int:plan_id>/', utilisateurs_views.checkout, name='checkout'),
    path('complete/<int:plan_id>/', utilisateurs_views.paymentcomplete, name="complete"),
    path('capture_navbar_data/', capture_navbar_data, name='capture_navbar_data'),
    path('display_navbar_data/<str:domaine>/<int:site_id>/', display_navbar_data, name="display_navbar_data"),
    path('save_navbar_html/<str:domaine>/<int:site_id>/', save_navbar_html, name="save_navbar_html"),


#######################################################################################################
# url pou sit blog yo
# #####################################################################################################

    path('dashboard_blog/<str:domaine>/', dashboard_blog, name='dashboard_blog'),
    path('marketplace/<str:domaine>/', marketplace, name='marketplace'),
    path('menu/<str:domaine>/', menu, name='menu'),
    path('manage/', manage, name='manage'),
    path('<str:domaine>/<int:site_id>/', view_site, name='view_site'),
    path('create_post/<int:site_id>/', create_post, name="create_post"),
    path('create_category/<int:site_id>/', create_category, name='create_category'),
    path('create_tag/<int:site_id>/', create_tag, name='create_tag'),
    path('<str:domaine>/<str:post_title>/<int:site_id>/<int:post_id>/', post_detail, name='post_detail'),
    path('submit_comment/<str:domaine>/<str:post_title>/<int:site_id>/<int:post_id>/', submit_comment, name='submit_comment'),
    path('<str:domaine>/<int:site_id>/register_blog', register_blog, name="register_blog"),
    path('<str:domaine>/<int:site_id>/signin_blog', signin_blog, name="signin_blog"),
    path('<str:domaine>/<int:site_id>/logout_blog', logout_blog, name='logout_blog'),
    path('DownloadResourcesView', DownloadResourcesView.as_view(), name='DownloadResourcesView'),
    path('pricing', pricing, name="pricing"),
    path('edit_post/<int:post_id>/', edit_post, name="edit_post"),
    path('edit_post_logic/<int:post_id>/', edit_post_logic, name='edit_post_logic'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('remove_like/<int:post_id>/', remove_like, name='remove_like'),
    path('search_post_in_site/<str:domaine>/<int:site_id>/', search_post_in_site, name="search_post_in_site"),
    path('category_posts/<str:domaine>/<int:site_id>/<int:category_id>/', category_posts, name="category_posts"),
    path('create_admin/<str:domaine>/', create_admin, name="create_admin"),
    path('create_admin_logic/<str:domaine>/<int:site_id>/', create_admin_logic, name="create_admin_logic"),
    path('design_header_site_blog/<str:domaine>/<int:site_id>/', design_header_site_blog, name="design_header_site_blog"),
    

#######################################################################################################
# url pou sit portfolio yo
# #####################################################################################################
    
    path('create_site_portofolio/<int:site_id>/', create_site_portofolio, name='create_site_portofolio'),
    path('dashboardportoo/<str:domaine>/', dashboardportofolio, name='dashboardportofolio'),
    path('view_site_portofolio/<str:domaine>/', view_site_portofolio, name='view_site_portofolio'),
    path('add_service/<str:domaine>/<int:site_id>/', add_service, name='add_service'),
    path('modif_service/<int:service_id>/', modif_service, name='modif_service'),
    
    path('add_info/<str:domaine>/<int:site_id>',add_info, name='add_info'),
    path('add_about/<str:domaine>/<int:site_id>/',add_about, name='add_about'),
    path('add_pro/<str:domaine>/<int:site_id>/',add_pro, name='add_pro'),
    path('add_hero/<str:domaine>/<int:site_id>/',add_hero, name='add_hero'),
    path('add_carriere/<str:domaine>/<int:site_id>/',add_carriere, name='add_carriere'),
    path('add_etude/<str:domaine>/<int:site_id>/',add_etude, name='add_etude'),
    path('add_skill/<str:domaine>/<int:site_id>/',add_skill, name='add_skill'),

    
    path('send_email/<int:site_id>/', send_email, name='send_email'),
    path('send_whatsapp/<int:site_id>/', send_whatsapp, name='send_whatsapp'),
    path('view_info/<str:domaine>/<int:site_id>',view_info, name='view_info'),
    path('view_service/<str:domaine>/<int:site_id>/', view_service, name='view_service'),
    path('contact/<int:site_id>/', contact_view, name='contact_view'),
    path('design_site/<str:domaine>/<int:site_id>/', design_site, name='design_site'),
    path('main_view/<str:domaine>/<int:site_id>/', main_view, name='main_view'),
    
#######################################################################################################
# url pou sit lekol yo
# #####################################################################################################
    
    path('create_site_school/<int:site_id>/', create_site_school, name='create_site_school'),
    path('dashboard_school/<str:domaine>/', dashboard_school, name='dashboard_school'),
    path('create_enseignant/<str:domaine>/<int:site_id>/', create_enseignant, name="create_enseignant"),
    path('create_enseignant_logic/<str:domaine>/<int:site_id>/', create_enseignant_logic, name="create_enseignant_logic"),
    path('create_examen_logic/<str:domaine>/<int:site_id>/', create_examen_logic, name="create_examen_logic"),
]