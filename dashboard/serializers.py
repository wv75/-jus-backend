from rest_framework import serializers
from .models import RelatorioPersonalizado, DashboardWidget, MetricaKPI, HistoricoMetrica, AlertaMetrica


class RelatorioPersonalizadoSerializer(serializers.ModelSerializer):
    usuario_criador_nome = serializers.CharField(source='usuario_criador.get_full_name', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    formato_display = serializers.CharField(source='get_formato_display', read_only=True)
    pode_editar = serializers.SerializerMethodField()
    
    class Meta:
        model = RelatorioPersonalizado
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'ultima_atualizacao']
    
    def get_pode_editar(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.usuario_criador == request.user
        return False


class DashboardWidgetSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    tamanho_display = serializers.CharField(source='get_tamanho_display', read_only=True)
    
    class Meta:
        model = DashboardWidget
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class MetricaKPISerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    tipo_calculo_display = serializers.CharField(source='get_tipo_calculo_display', read_only=True)
    valor_atual = serializers.SerializerMethodField()
    status_meta = serializers.SerializerMethodField()
    
    class Meta:
        model = MetricaKPI
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_valor_atual(self, obj):
        # Buscar o último valor calculado
        ultimo_historico = HistoricoMetrica.objects.filter(metrica=obj).order_by('-data_calculo').first()
        return float(ultimo_historico.valor) if ultimo_historico else 0
    
    def get_status_meta(self, obj):
        if not obj.meta:
            return None
        
        valor_atual = self.get_valor_atual(obj)
        if valor_atual >= obj.meta:
            return 'atingida'
        elif valor_atual >= obj.meta * 0.8:
            return 'proxima'
        else:
            return 'distante'


class HistoricoMetricaSerializer(serializers.ModelSerializer):
    metrica_nome = serializers.CharField(source='metrica.nome', read_only=True)
    variacao_percentual = serializers.FloatField(read_only=True)
    
    class Meta:
        model = HistoricoMetrica
        fields = '__all__'
        read_only_fields = ['created_at']


class AlertaMetricaSerializer(serializers.ModelSerializer):
    metrica_nome = serializers.CharField(source='metrica.nome', read_only=True)
    tipo_alerta_display = serializers.CharField(source='get_tipo_alerta_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    usuario_responsavel_nome = serializers.CharField(source='usuario_responsavel.get_full_name', read_only=True)
    dias_ativo = serializers.SerializerMethodField()
    
    class Meta:
        model = AlertaMetrica
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_dias_ativo(self, obj):
        if obj.status == 'ativo':
            from django.utils import timezone
            delta = timezone.now() - obj.created_at
            return delta.days
        return 0
