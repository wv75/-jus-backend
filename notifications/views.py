from rest_framework import viewsets, permissions
from .models import NotificationLog, Notification
from .serializers import NotificationLogSerializer, NotificationSerializer

class NotificationLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar e editar os logs de notificação.
    """
    # <<< CORREÇÃO: Trocamos 'timestamp' por 'created_at', que existe no modelo.
    queryset = NotificationLog.objects.all().order_by('-created_at')
    serializer_class = NotificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para as notificações internas do sistema.
    """
    # Aparentemente seu modelo Notification TEM o campo 'timestamp', então mantemos aqui.
    queryset = Notification.objects.all().order_by('-timestamp')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]