
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import create_admin_view, editar_producto, borrar_producto, actualizar_precios


urlpatterns = [
    path('', views.index, name= 'index'),
    
    path('account/login/', auth_views.LoginView.as_view(template_name="pet/registration/login.html"),name='login'),
    path('account/logout/', views.cerrar_logout,name='logout'),
    
    path('account/password_reset/', auth_views.PasswordResetView.as_view(template_name="pet/registration/password_reset.html"),name='password_reset'),
    
    # path('acounts/', include(django.contrib.auth.urls)),
    # path('listado_articulos', views.listado_articulos, name='listado_articulos'),
    path('alta_producto', views.alta_producto, name='alta_producto'),
    path('listado_articulos',views.ArticuloListView.as_view(),name='listado_articulos'),

    path('create-admin/', create_admin_view, name='create_admin'),  # URL para crear un nuevo administrador
     
# ---------------------------------------------------------------------------------------------------------------------
     path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='pet/registration/password_reset_form.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='pet/registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='pet/registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='pet/registration/password_reset_complete.html'), 
         name='password_reset_complete'),
    # otras URLs

    path('editar/<int:pk>/', editar_producto, name='editar_producto'),
    path('borrar/<int:pk>/', borrar_producto, name='borrar_producto'),
    path('actualizar_precios/', actualizar_precios, name='actualizar_precios'),
]

