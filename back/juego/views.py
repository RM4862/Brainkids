
from rest_framework import viewsets, status
from rest_framework.response import Response
import requests
from .models import Usuario, Mascota, Recompensa, Recurso,Cuento, Linea
from .models import Pictograma
from .serializers import UsuarioSerializer, MascotaSerializer, RecompensaSerializer, RecursoSerializer
from .serializers import  CuentoSerializer, LineaSerializer, PictogramaSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def usuario_login(request):
    usuario = request.data.get('usuario')
    contrasena = request.data.get('contraseña')
    if not usuario or not contrasena:
        return Response({'error': 'Usuario y contraseña requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Usuario.objects.get(usuario=usuario)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Si la contraseña está hasheada, usa check_password. Si no, compara directamente.
    if user.contraseña == contrasena or check_password(contrasena, user.contraseña):
        serializer = UsuarioSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)

class UsuarioViewSet(viewsets.ModelViewSet):
        queryset = Usuario.objects.all()
        serializer_class = UsuarioSerializer

        def create(self, request, *args, **kwargs):
            # Si el usuario viene de OAuth, la contraseña puede ser None o generada
            from django.contrib.auth.hashers import make_password
            data = request.data.copy()
            if 'contraseña' in data:
                data['contraseña'] = make_password(data['contraseña'])
            if 'oauth' in data and data['oauth']:
                data['contraseña'] = ''  # O genera una contraseña aleatoria
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

class RecompensaViewSet(viewsets.ModelViewSet):
    queryset = Recompensa.objects.all()
    serializer_class = RecompensaSerializer

class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer

class CuentoViewSet(viewsets.ModelViewSet):
    queryset = Cuento.objects.all()
    serializer_class = CuentoSerializer
    
class LineaViewSet(viewsets.ModelViewSet):
    queryset = Linea.objects.all()
    serializer_class = LineaSerializer

    def get_queryset(self):
        cuento_id = self.request.query_params.get('cuento')
        if cuento_id:
            return Linea.objects.filter(cuento_id=cuento_id)
        return Linea.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Obtener la línea recién creada
        if response.status_code == 201:
            linea_id = response.data.get('id_linea')
            from .models import Linea, Pictograma
            import requests, re
            linea = Linea.objects.get(id_linea=linea_id)
            texto = linea.contenido_lin
            palabras = re.findall(r'\w+', texto.lower())
            for palabra in palabras:
                url = f"https://api.arasaac.org/api/pictograms/es/search/{palabra}"
                pictogramas_res = requests.get(url)
                if pictogramas_res.status_code == 200:
                    data = pictogramas_res.json()
                    if data:
                        pictograma_id = data[0]['_id']
                        pictograma_url = f"https://static.arasaac.org/pictograms/{pictograma_id}/{pictograma_id}_500.png"
                        Pictograma.objects.create(
                            id_pic=str(pictograma_id),
                            linea=linea,
                            texto_original=palabra,
                            url_imagen=pictograma_url
                        )
        return response
    
class PictogramaViewSet(viewsets.ModelViewSet):
    queryset = Pictograma.objects.all()
    serializer_class = PictogramaSerializer

    def create(self, request, *args, **kwargs):
        linea_id = request.data.get('linea')
        try:
            linea = Linea.objects.get(pk=linea_id)
        except Linea.DoesNotExist:
            return Response({'error': 'Línea no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        texto = linea.contenido_lin

        # Consumir la API de ARASAAC
        url = f'https://api.arasaac.org/v1/pictograms/text/{texto}?language=es'
        response = requests.get(url)
        if response.status_code == 200:
            pictogramas = response.json()
            pictogramas_creados = []
            for pictograma in pictogramas:
                id_pic = str(pictograma['id'])
                url_imagen = pictograma['url']
                pictograma_obj = Pictograma.objects.create(
                    id_pic=id_pic,
                    linea=linea,
                    texto_original=texto,
                    url_imagen=url_imagen
                )
                pictogramas_creados.append(pictograma_obj)
            serializer = self.get_serializer(pictogramas_creados, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No se pudo obtener pictogramas'}, status=status.HTTP_400_BAD_REQUEST)