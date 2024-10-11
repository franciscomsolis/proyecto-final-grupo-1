from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Articulo, Categoria, Comentario, Contacto
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ArticuloForm, ComentarioForm, ContactoForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail 
from django.contrib.auth.models import Group
# Vista de la página de inicio
def inicio(request):
    orden = request.GET.get('orden', 'fecha')  # Por defecto ordena por fecha

    if orden == 'fecha':
        articulos = Articulo.objects.all().order_by('-fecha_publicacion')  # Últimos artículos
    elif orden == 'alfabetico':
        articulos = Articulo.objects.all().order_by('titulo')  # Orden alfabético

    return render(request, 'blog_app/inicio.html', {'articulos': articulos})

# Vista de la página de categorías
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'blog_app/categorias.html', {'categorias': categorias})

# Vista para mostrar artículos por categoría
def articulos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    articulos = Articulo.objects.filter(categoria=categoria)
    return render(request, 'blog_app/articulos_por_categoria.html', {'categoria': categoria, 'articulos': articulos})

# Vista de la página 'Acerca de'
def acerca_de(request):
    return render(request, 'blog_app/acerca_de.html')

# Vista de la página de contacto
def contacto(request):
    return render(request, 'blog_app/contacto.html')

# Vista para mostrar un artículo individual
def detalle_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    return render(request, 'blog_app/detalle_articulo.html', {'articulo': articulo})

# Vista para crear un artículo (solo Colaboradores)
def es_colaborador(user):
    return user.is_authenticated and user.groups.filter(name='Colaboradores').exists()


@login_required
@user_passes_test(es_colaborador)
def crear_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)  # request.FILES para manejar archivos
        if form.is_valid():
            nuevo_articulo = form.save(commit=False)
            nuevo_articulo.autor = request.user
            nuevo_articulo.save()
            return redirect('detalle_articulo', articulo_id=nuevo_articulo.id)
    else:
        form = ArticuloForm()
    return render(request, 'blog_app/crear_articulo.html', {'form': form})



#@login_required
#@user_passes_test(es_colaborador)
def editar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('detalle_articulo', articulo_id=articulo.id)
    else:
        form = ArticuloForm(instance=articulo)

    return render(request, 'blog_app/editar_articulo.html', {'form': form, 'articulo': articulo})



#@login_required
#@user_passes_test(es_colaborador)
def eliminar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method == 'POST':
        articulo.delete()
        return redirect('inicio')  # Redirige a la página de inicio tras la eliminación

    return render(request, 'blog_app/eliminar_articulo.html', {'articulo': articulo})



# Agregar comentario a un artículo
@login_required
def agregar_comentario(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = articulo
            comentario.autor = request.user  # Asigna el usuario que hace el comentario
            comentario.save()
            return redirect('detalle_articulo', articulo_id=articulo.id)
    else:
        form = ComentarioForm()
    return render(request, 'blog_app/agregar_comentario.html', {'form': form, 'articulo': articulo})

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.autor != request.user:
        return redirect('detalle_articulo', articulo_id=comentario.articulo.id)  # Redirige si no es el autor

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('detalle_articulo', articulo_id=comentario.articulo.id)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'blog_app/editar_comentario.html', {'form': form})

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.autor != request.user:
        return redirect('detalle_articulo', articulo_id=comentario.articulo.id)  # Redirige si no es el autor

    if request.method == 'POST':
        comentario.delete()
        return redirect('detalle_articulo', articulo_id=comentario.articulo.id)
    return render(request, 'blog_app/eliminar_comentario.html', {'comentario': comentario})

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al login tras el registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Opción 1: Enviar correo electrónico
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']
            
            send_mail(
                f"Nuevo mensaje de {nombre}",  # Asunto del correo
                mensaje,  # Mensaje
                email,  # De
                [settings.EMAIL_HOST_USER],  # Para (equipo de blog)
            )
            
            # Opción 2: Guardar en la base de datos (si usas el modelo)
            # form.save()
            
            return redirect('contacto_exito')  # Redirige a una página de éxito
    else:
        form = ContactoForm()
    
    return render(request, 'contacto.html', {'form': form})
# views.py
def contacto_exito(request):
    return render(request, 'contacto_exito.html')

