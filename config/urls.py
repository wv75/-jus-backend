# config/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from core.views import landing_view, vue_app_view, LogoutAPIView

# ==============================================================================
# 1. IMPORTAR AS VIEWSETS E VIEWS
# ==============================================================================
from clientes.views import ClienteViewSet
from processos.views import ProcessoViewSet
from documentos.views import DocumentoViewSet

# --- CORREÇÃO: Importar o UserManagementViewSet ---
from accounts.views import (
    AdvogadoViewSet,
    UserDetailsAPIView,
    AdvogadoCreateView,
    UserManagementViewSet  # <-- 1. IMPORTAÇÃO ADICIONADA
)


# ==============================================================================
# 2. CONFIGURAÇÃO DO ROUTER DA API
# ==============================================================================
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'processos', ProcessoViewSet, basename='processo')
router.register(r'documentos', DocumentoViewSet, basename='documento')

# Endpoint para DROPDOWNS (usa AdvogadoSimpleSerializer)
router.register(r'advogados', AdvogadoViewSet, basename='advogado') 

# --- CORREÇÃO: Registrar o novo endpoint de Gestão ---
# Endpoint para GESTÃO DE USUÁRIOS (usa AdvogadoListSerializer)
router.register(r'user-management', UserManagementViewSet, basename='user-management') # <-- 2. REGISTRO ADICIONADO


# ==============================================================================
# 3. CONFIGURAÇÃO FINAL DAS URLs DO PROJETO
# ==============================================================================
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_view, name='landing'),

    # --- APIs de Autenticação e Usuário ---
    path('api/v1/auth/login/', obtain_auth_token, name='api-login'),
    path('api/v1/auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/v1/auth/user/', UserDetailsAPIView.as_view(), name='api-user-details'),

    # --- API de Criação de Advogado (Correto, antes do router) ---
    # Esta é a rota "específica". Deve vir primeiro.
    path('api/v1/advogados/create/', AdvogadoCreateView.as_view(), name='advogado-create'),

    # --- APIs do Router (GENÉRICO) ---
    # Esta rota "genérica" vem DEPOIS da rota específica.
    # Agora ela inclui /user-management/
    path('api/v1/', include(router.urls)), 

    # --- Outras APIs (se houver) ---
    path('api-auth/', include('rest_framework.urls')), 

    # --- O "CATCH-ALL" do Vue (DEVE SER A ÚLTIMA URL) ---
    re_path(r'^.*$', vue_app_view, name='vue-app'),

]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)