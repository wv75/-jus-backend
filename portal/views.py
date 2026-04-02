from rest_framework import serializers
from andamentos.models import AndamentoProcessual

class AndamentoProcessualDashboardSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para exibir os últimos andamentos no dashboard.
    """
    processo_numero = serializers.CharField(source='processo.numero_processo', read_only=True)
    cliente_nome = serializers.CharField(source='processo.cliente.nome', read_only=True)

    class Meta:
        model = AndamentoProcessual
        fields = [
            'id', 'titulo', 'data_evento', 'created_at', 
            'processo_numero', 'cliente_nome'
        ]
