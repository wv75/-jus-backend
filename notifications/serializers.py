from rest_framework import serializers
from .models import NotificationLog, Notification


class NotificationLogSerializer(serializers.ModelSerializer):
    """Serializer para os logs de notificação."""
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True, default=None)
    processo_numero = serializers.CharField(source='processo.numero_processo', read_only=True, default=None)

    class Meta:
        model = NotificationLog
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para as notificações internas do sistema."""
    timesince = serializers.CharField(source='timesince', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'verb', 'description', 'tipo', 'unread', 
            'timestamp', 'timesince'
        ]

