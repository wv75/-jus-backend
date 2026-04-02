from rest_framework import serializers
from .models        import Fornecedor


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Fornecedor
        fields           = [
            'id', 'ativo', 'nome', 'documento', 
            'contato', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']