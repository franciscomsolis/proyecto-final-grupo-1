from django.db import models
from django.contrib.auth.models import User

# Modelo de Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo de Artículo
class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con usuario
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)  # Categoría del artículo
    imagen = models.ImageField(upload_to='articulos/', blank=True, null=True)

    class Meta:
        permissions = [
            ("can_edit_article", "Puede editar artículo"),
            ("can_delete_article", "Puede eliminar artículo"),
        ]
def __str__(self):
        return self.titulo        

# Modelo de Comentarios
class Comentario(models.Model):
    articulo = models.ForeignKey(Articulo, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor} en {self.articulo}'

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre   