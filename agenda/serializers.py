from rest_framework import serializers
from .models import TipoCompromisso, Compromisso


class TipoCompromissoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCompromisso
        fields = '__all__'
        read_only_fields = ['created_at']


class CompromissoSerializer(serializers.ModelSerializer):
    tipo_nome = serializers.CharField(source='tipo.nome', read_only=True)
    tipo_cor = serializers.CharField(source='tipo.cor', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    processo_numero = serializers.CharField(source='processo.numero_processo', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    participantes_nomes = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    duracao_minutos = serializers.IntegerField(read_only=True)
    is_hoje = serializers.BooleanField(read_only=True)
    is_passado = serializers.BooleanField(read_only=True)
    is_proximo = serializers.BooleanField(read_only=True)
    cor_prioridade = serializers.CharField(read_only=True)
    
    class Meta:
        model = Compromisso
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_participantes_nomes(self, obj):
        return [p.get_full_name() or p.username for p in obj.participantes.all()]


# Serializers para PrazoProcessual e AlertaEnviado serão implementados quando os modelos forem criados
