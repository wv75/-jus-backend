from rest_framework import serializers
from .models import TemplateMensagem


class TemplateMensagemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TemplateMensagem
        fields = [
            'id', 'canal', 'evento', 'linguagem', 'conteudo',
            'ativo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
