
# juego/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import UsuarioViewSet, MascotaViewSet, RecompensaViewSet, RecursoViewSet
from .views import CuentoViewSet, LineaViewSet, PictogramaViewSet, usuario_login

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'mascotas', MascotaViewSet)
router.register(r'recompensas', RecompensaViewSet)
router.register(r'recursos', RecursoViewSet)
router.register(r'cuentos', CuentoViewSet)
router.register(r'lineas', LineaViewSet)
router.register(r'pictogramas', PictogramaViewSet)

urlpatterns = [
    path('login/', usuario_login),  # <-- login fuera del router
    path('', include(router.urls)),
]