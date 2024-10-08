from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/<int:categoria_id>/', views.articulos_por_categoria, name='articulos_por_categoria'),
    path('acerca_de/', views.acerca_de, name='acerca_de'),
    path('contacto/', views.contacto, name='contacto'),
    path('articulo/<int:articulo_id>/', views.detalle_articulo, name='detalle_articulo'),
    path('articulo/crear/', views.crear_articulo, name='crear_articulo'),
    path('articulo/<int:articulo_id>/editar/', views.editar_articulo, name='editar_articulo'),
    path('articulo/<int:articulo_id>/eliminar/', views.eliminar_articulo, name='eliminar_articulo'),
    path('articulo/<int:articulo_id>/comentario/', views.agregar_comentario, name='agregar_comentario'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('contacto/exito/', views.contacto_exito, name='contacto_exito'),
]
