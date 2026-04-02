from django.urls            import path, include
from rest_framework.routers import DefaultRouter
from .                      import views


app_name    = 'fornecedores'
router      = DefaultRouter()

router.register(r'fornecedores', views.FornecedorViewSet, basename='fornecedores')

urlpatterns = [
    path('', include(router.urls)),
]