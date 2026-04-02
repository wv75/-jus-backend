from django.urls            import path, include
from rest_framework.routers import DefaultRouter
from .                      import views

app_name    = 'accounts'
router      = DefaultRouter()

router.register(r'user-management', views.UserManagementViewSet, basename='user-management')
router.register(r'advogados', views.AdvogadoViewSet, basename='advogados')

urlpatterns = [
    path('me/', views.UserDetailsAPIView.as_view(), name='user-details'),
    path('advogado-create/', views.AdvogadoCreateView.as_view(), name='advogado-create'),
    path('', include(router.urls)),
]