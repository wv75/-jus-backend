from django.urls            import path, include
from rest_framework.routers import DefaultRouter
from .                      import views


app_name    = 'documentos'
router      = DefaultRouter()

router.register(r'categorias', views.CategoriaDocumentoViewSet, basename='categorias')
router.register(r'documentos', views.DocumentoViewSet, basename='documentos')
router.register(r'templates', views.TemplateDocumentoViewSet, basename='templates')
router.register(r'assinaturas', views.AssinaturaDigitalViewSet, basename='assinaturas')

urlpatterns = [
    path('', include(router.urls)),
]