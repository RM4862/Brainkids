
from rest_framework import serializers
from .models import Usuario, Mascota, Recompensa,Recurso, Cuento
from .models import Linea, Pictograma

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 'nombre', 'usuario', 'correo', 'contraseña',
            'tutor_nombre', 'tutor_correo', 'fecha_nacimiento'
        ]
class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = ['id_nom_masc', 'img_masc']
        
class RecompensaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recompensa
        fields = ['id_recompensa', 'fecha_recompensa', 'estado']
        

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = ['id_recurso', 'vidas', 'monedas', 'energia', 'cant_alimentos']
        
class CuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuento
        fields = ['id_cuento', 'titulo', 'estado_leido']

class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linea
        fields = ['id_linea', 'contenido_lin', 'cuento']

class PictogramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictograma
        fields = ['id_pic', 'linea', 'texto_original', 'url_imagen']