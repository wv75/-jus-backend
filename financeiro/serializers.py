from rest_framework import serializers
from .models        import PlanoContas, ContaBancaria, MovimentacaoFinanceira, Honorario


class PlanoContasSerializer(serializers.ModelSerializer):
    conta_pai_nome = serializers.CharField(source='conta_pai.nome', read_only=True)

    class Meta:
        model            = PlanoContas
        fields           = [
            'id', 'ativo', 'codigo', 'nome', 'tipo', 'conta_pai', 
            'conta_pai_nome', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model            = ContaBancaria
        fields           = [
            'id', 'ativo', 'nome', 'banco', 'agencia', 'conta', 
            'saldo_inicial', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MovimentacaoFinanceiraSerializer(serializers.ModelSerializer):
    plano_conta_nome     = serializers.CharField(source='plano_conta.nome', read_only=True)
    conta_bancaria_nome  = serializers.CharField(source='conta_bancaria.nome', read_only=True)
    cliente_nome         = serializers.CharField(source='cliente.nome', read_only=True)
    fornecedor_nome      = serializers.CharField(source='fornecedor.nome', read_only=True)
    processo_numero      = serializers.CharField(source='processo.numero_processo', read_only=True)
    responsavel_nome     = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    tipo_display         = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display       = serializers.CharField(source='get_status_display', read_only=True)
    parcelamento_display = serializers.CharField(source='get_parcelamento_display', read_only=True)

    class Meta:
        model            = MovimentacaoFinanceira
        fields           = [
            'id', 'ativo', 'tipo', 'tipo_display', 'descricao', 'valor', 'data_registro',
            'data_vencimento', 'data_pagamento', 'parcelamento', 'parcelamento_display',
            'vigencia_inicio', 'vigencia_fim', 'competencia_inicio', 'competencia_fim',
            'conta_bancaria', 'conta_bancaria_nome', 'plano_conta', 'plano_conta_nome',
            'cliente', 'cliente_nome', 'fornecedor', 'fornecedor_nome', 'processo',
            'processo_numero', 'status', 'status_display', 'observacoes', 'comprovante',
            'responsavel', 'responsavel_nome', 'numero_documento', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'data_registro', 'created_at', 'updated_at']


class HonorarioSerializer(serializers.ModelSerializer):
    processo_numero       = serializers.CharField(source='processo.numero_processo', read_only=True)
    cliente_nome          = serializers.CharField(source='cliente.nome', read_only=True)
    advogado_nome         = serializers.CharField(source='advogado.get_full_name', read_only=True)
    tipo_display          = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display        = serializers.CharField(source='get_status_display', read_only=True)
    valor_total_calculado = serializers.ReadOnlyField(source='valor_total')

    class Meta:
        model            = Honorario
        fields           = [
            'id', 'ativo', 'cliente', 'cliente_nome', 'processo', 'processo_numero',
            'descricao', 'tipo', 'tipo_display', 'valor', 'percentual', 'valor_hora',
            'horas_trabalhadas', 'data_orcamento', 'data_aprovacao', 'data_vencimento',
            'status', 'status_display', 'observacoes', 'advogado', 'advogado_nome',
            'numero_documento', 'valor_total_calculado', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'data_orcamento', 'created_at', 'updated_at']