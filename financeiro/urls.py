from django.urls            import path, include
from rest_framework.routers import DefaultRouter
from .                      import views


app_name    = 'financeiro'
router      = DefaultRouter()

router.register(r'plano-contas', views.PlanoContasViewSet, basename='plano-contas')
router.register(r'contas-bancarias', views.ContaBancariaViewSet, basename='contas-bancarias')
router.register(r'movimentacoes', views.MovimentacaoFinanceiraViewSet, basename='movimentacoes')
router.register(r'honorarios', views.HonorarioViewSet, basename='honorarios')
router.register(r'resumo', views.ResumoFinanceiroViewSet, basename='resumo-financeiro')

urlpatterns = [
    path('', include(router.urls)),
]