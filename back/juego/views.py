
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
	queryset = Usuario.objects.all()
	serializer_class = UsuarioSerializer

	def create(self, request, *args, **kwargs):
		# Si el usuario viene de OAuth, la contraseña puede ser None o generada
		data = request.data.copy()
		if 'oauth' in data and data['oauth']:
			data['contraseña'] = ''  # O genera una contraseña aleatoria
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
