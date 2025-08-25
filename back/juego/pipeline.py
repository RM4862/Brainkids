from .models import Usuario

def create_usuario(strategy, details, user=None, *args, **kwargs):
    correo = details.get('email')
    nombre = details.get('fullname') or details.get('username')
    if correo and not Usuario.objects.filter(correo=correo).exists():
        Usuario.objects.create(nombre=nombre, correo=correo, contraseña='')
