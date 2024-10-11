from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('categorias/', views.categorias, name='categorias'),  # Página de categorías
    path('categoria/<int:categoria_id>/', views.articulos_por_categoria, name='articulos_por_categoria'),  # Artículos por categoría
    path('acerca_de/', views.acerca_de, name='acerca_de'),  # Página Acerca de
    path('contacto/', views.contacto, name='contacto'),  # Página de contacto
    path('contacto/exito/', views.contacto_exito, name='contacto_exito'),  # Página de éxito tras enviar el contacto
    
    # Detalle de artículo
    path('articulo/<int:articulo_id>/', views.detalle_articulo, name='detalle_articulo'),  
    
    # Crear, editar, eliminar artículo (solo colaboradores)
    path('articulo/nuevo/', views.crear_articulo, name='crear_articulo'),  # Crear artículo
    path('articulo/<int:articulo_id>/editar/', views.editar_articulo, name='editar_articulo'),  # Editar artículo
    path('articulo/<int:articulo_id>/eliminar/', views.eliminar_articulo, name='eliminar_articulo'),  # Eliminar artículo

    # Comentarios
    path('articulo/<int:articulo_id>/comentar/', views.agregar_comentario, name='agregar_comentario'),  # Agregar comentario
    path('comentario/<int:comentario_id>/editar/', views.editar_comentario, name='editar_comentario'),  # Editar comentario
    path('comentario/<int:comentario_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),  # Eliminar comentario

    # Autenticación
    path('registro/', views.registro_usuario, name='registro'),  # Registro de usuario
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('accounts/', include('django.contrib.auth.urls')),
]


