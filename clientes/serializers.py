from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    primeiro_nome = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'documento', 'email', 'telefone_whatsapp',
            'consentimento_lgpd', 'data_consentimento', 'canal_preferido',
            'ativo', 'primeiro_nome', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'data_consentimento', 'created_at', 'updated_at']


class ClienteSimpleSerializer(serializers.ModelSerializer):
    """Serializer simplificado para uso em nested relationships"""
    
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'telefone_whatsapp', 'consentimento_lgpd']
