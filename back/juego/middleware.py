
from .models import Usuario

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Código antes de la vista
        response = self.get_response(request)
        # Código después de la vista
        return response
    
#Middleware para crear usuarios por OAuth de google
class OAuthUserCreationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ejemplo: Si la petición contiene datos de OAuth, crear usuario si no existe
        oauth_data = request.session.get('oauth_data')
        if oauth_data:
            correo = oauth_data.get('correo')
            nombre = oauth_data.get('nombre', '')
            if correo and not Usuario.objects.filter(correo=correo).exists():
                Usuario.objects.create(nombre=nombre, correo=correo, contraseña='')
        response = self.get_response(request)
        return response
