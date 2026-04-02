from rest_framework       import serializers
from .models              import AndamentoProcessual
from clientes.serializers import ClienteSimpleSerializer


class AndamentoProcessualSerializer(serializers.ModelSerializer):
    processo_numero = serializers.CharField(source='processo.numero_processo', read_only=True)
    cliente         = ClienteSimpleSerializer(source='processo.cliente', read_only=True)
    data_evento_fmt = serializers.ReadOnlyField()

    class Meta:
        model            = AndamentoProcessual
        fields           = [
            'id', 'ativo', 'processo', 'processo_numero', 'cliente', 'tipo_evento',
            'titulo', 'descricao', 'data_evento', 'data_evento_fmt',
            'prazo_limite', 'publicado_para_cliente', 'canal_enviado',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AndamentoProcessualSimpleSerializer(serializers.ModelSerializer):
    processo_numero = serializers.CharField(source='processo.numero_processo', read_only=True)

    class Meta:
        model  = AndamentoProcessual
        fields = [
            'id', 'ativo', 'processo_numero', 'tipo_evento', 'titulo',
            'data_evento', 'publicado_para_cliente'
        ]