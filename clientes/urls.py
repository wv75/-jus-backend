from django.urls            import path, include
from rest_framework.routers import DefaultRouter
from .                      import views


app_name = 'clientes'
router   = DefaultRouter()

router.register(r'pessoas-fisicas', views.PessoaFisicaViewSet, basename='pessoas-fisicas')
router.register(r'pessoas-juridicas', views.PessoaJuridicaViewSet, basename='pessoas-juridicas')

urlpatterns = [
    path('clientes/', include(router.urls)),
]