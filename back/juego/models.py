
from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    tutor_nombre = models.CharField(max_length=100)
    tutor_correo = models.EmailField()
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.usuario

class Mascota(models.Model):
    id_nom_masc = models.CharField(max_length=50, primary_key=True)
    img_masc = models.ImageField(upload_to='mascotas/')
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='mascota')

    def __str__(self):
        return self.id_nom_masc
    
class Recompensa(models.Model):
    id_recompensa = models.CharField(max_length=25, primary_key=True)
    fecha_recompensa = models.DateField()
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.id_recompensa
    
class Recurso(models.Model):
    id_recurso = models.CharField(max_length=25, primary_key=True)
    vidas = models.IntegerField()
    monedas = models.IntegerField()
    energia = models.IntegerField()
    cant_alimentos = models.IntegerField()

    def __str__(self):
        return self.id_recurso

class Cuento(models.Model):
    id_cuento = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    estado_leido = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
    
class Linea(models.Model):
    id_linea = models.CharField(max_length=10, primary_key=True)
    contenido_lin = models.CharField(max_length=300)
    cuento = models.ForeignKey('Cuento', on_delete=models.CASCADE, related_name='lineas')

    def __str__(self):
        return self.id_linea

class Pictograma(models.Model):
    id_pic = models.CharField(max_length=10, primary_key=True)
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, related_name='pictogramas')
    texto_original = models.CharField(max_length=300)
    url_imagen = models.URLField()  # URL de la imagen del pictograma

    def __str__(self):
        return self.id_pic