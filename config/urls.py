from django.contrib                 import admin
from django.urls                    import path, include, re_path
from django.conf                    import settings
from django.conf.urls.static        import static
from rest_framework.routers         import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from core.views                     import landing_view, vue_app_view, LogoutAPIView
from processos.views                import ProcessoViewSet
from accounts.views                 import AdvogadoViewSet, UserDetailsAPIView, AdvogadoCreateView, UserManagementViewSet


router = DefaultRouter()

router.register(r'processos', ProcessoViewSet, basename='processo')
router.register(r'advogados', AdvogadoViewSet, basename='advogado')
router.register(r'user-management', UserManagementViewSet, basename='user-management')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_view, name='landing'),
    
    path('api/v1/auth/login/', obtain_auth_token, name='api-login'),
    path('api/v1/auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/v1/auth/user/', UserDetailsAPIView.as_view(), name='api-user-details'),
    
    path('api/v1/', include('clientes.urls')),
    path('api/v1/', include('documentos.urls')),
    path('api/v1/advogados/create/', AdvogadoCreateView.as_view(), name='advogado-create'),
    path('api/v1/', include(router.urls)),
    
    path('api-auth/', include('rest_framework.urls')),
    
    re_path(r'^.*$', vue_app_view, name='vue-app'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)