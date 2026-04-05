from rest_framework             import serializers
from django.contrib.auth.models import User
from .models                    import Processo
from clientes.models            import Cliente
from clientes.serializers       import ClienteBaseSerializer


class ProcessoSerializer(serializers.ModelSerializer):
    cliente              = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    advogado_responsavel = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True), allow_null=True, required=False)
    status_display       = serializers.CharField(source='get_status_display', read_only=True)
    risco_display        = serializers.CharField(source='get_risco_display', read_only=True)
    prioridade_display   = serializers.CharField(source='get_prioridade_display', read_only=True)

    class Meta:
        model            = Processo
        fields           = [
            'id', 'ativo', 'numero_processo', 'cliente', 'tarefa', 'foro', 'vara',
            'comarca', 'classe', 'assunto', 'parte_contraria', 'advogado_responsavel',
            'situacao_atual', 'status', 'status_display', 'risco', 'risco_display', 
            'prioridade', 'prioridade_display', 'prazo_final', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProcessoListSerializer(serializers.ModelSerializer):
    cliente_nome       = serializers.SerializerMethodField()
    advogado_nome      = serializers.CharField(source='advogado_responsavel.get_full_name', read_only=True)
    status_display     = serializers.CharField(source='get_status_display', read_only=True)
    risco_display      = serializers.CharField(source='get_risco_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)

    class Meta:
        model            = Processo
        fields           = [
            'id', 'ativo', 'numero_processo', 'assunto', 'cliente_nome',
            'advogado_nome', 'status', 'status_display', 'risco', 
            'risco_display', 'prioridade', 'prioridade_display', 'prazo_final'
        ]
        read_only_fields = fields

    def get_cliente_nome(self, obj):
        if hasattr(obj.cliente, 'pf'):
            return obj.cliente.pf.nome_completo
        if hasattr(obj.cliente, 'pj'):
            return obj.cliente.pj.razao_social
        return f"Cliente {obj.cliente_id}"


class ProcessoDetailSerializer(ProcessoSerializer):
    cliente = ClienteBaseSerializer(read_only=True)

    class Meta(ProcessoSerializer.Meta):
        pass