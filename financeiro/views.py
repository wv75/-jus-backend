from rest_framework                import viewsets, status, filters
from rest_framework.decorators     import action
from rest_framework.response       import Response
from rest_framework.permissions    import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models              import Sum, Case, When, DecimalField
from decimal                       import Decimal
from django.utils                  import timezone

from .models                       import PlanoContas, ContaBancaria, MovimentacaoFinanceira, Honorario, TipoMovimentacaoChoices, StatusMovimentacaoChoices, StatusHonorarioChoices
from .serializers                  import PlanoContasSerializer, ContaBancariaSerializer, MovimentacaoFinanceiraSerializer, HonorarioSerializer


class PlanoContasViewSet(viewsets.ModelViewSet):
    queryset           = PlanoContas.objects.ativos()
    serializer_class   = PlanoContasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['tipo', 'ativo']
    search_fields      = ['codigo', 'nome']
    ordering_fields    = ['codigo', 'nome', 'tipo']
    ordering           = ['codigo']


class ContaBancariaViewSet(viewsets.ModelViewSet):
    queryset           = ContaBancaria.objects.ativos()
    serializer_class   = ContaBancariaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['ativo', 'banco']
    search_fields      = ['nome', 'banco', 'agencia', 'conta']
    ordering_fields    = ['nome', 'banco']
    ordering           = ['nome']


class MovimentacaoFinanceiraViewSet(viewsets.ModelViewSet):
    queryset           = MovimentacaoFinanceira.objects.ativos().select_related('conta_bancaria', 'plano_conta', 'cliente', 'fornecedor', 'processo', 'responsavel')
    serializer_class   = MovimentacaoFinanceiraSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['tipo', 'status', 'conta_bancaria', 'plano_conta', 'cliente']
    search_fields      = ['descricao', 'observacoes']
    ordering_fields    = ['data_vencimento', 'data_pagamento', 'valor']
    ordering           = ['-data_vencimento']

    def perform_create(self, serializer):
        serializer.save(responsavel=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_como_pago(self, request, pk=None):
        movimentacao                = self.get_object()
        movimentacao.status         = StatusMovimentacaoChoices.PAGO
        movimentacao.data_pagamento = timezone.now().date()
        movimentacao.save()
        serializer                  = self.get_serializer(movimentacao)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HonorarioViewSet(viewsets.ModelViewSet):
    queryset           = Honorario.objects.ativos().select_related('cliente', 'processo', 'advogado')
    serializer_class   = HonorarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['tipo', 'status', 'cliente', 'advogado']
    search_fields      = ['descricao', 'observacoes']
    ordering_fields    = ['data_orcamento', 'data_vencimento', 'valor']
    ordering           = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(advogado=self.request.user)

    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        honorario                = self.get_object()
        honorario.status         = StatusHonorarioChoices.APROVADO
        honorario.data_aprovacao = timezone.now().date()
        honorario.save()
        serializer               = self.get_serializer(honorario)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResumoFinanceiroViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        totais = MovimentacaoFinanceira.objects.ativos().aggregate(
            receitas_pagas = Sum(Case(When(tipo=TipoMovimentacaoChoices.RECEITA, status=StatusMovimentacaoChoices.PAGO, then='valor'), default=0, output_field=DecimalField())),
            despesas_pagas = Sum(Case(When(tipo=TipoMovimentacaoChoices.DESPESA, status=StatusMovimentacaoChoices.PAGO, then='valor'), default=0, output_field=DecimalField())),
            contas_receber = Sum(Case(When(tipo=TipoMovimentacaoChoices.RECEITA, status=StatusMovimentacaoChoices.PENDENTE, then='valor'), default=0, output_field=DecimalField())),
            contas_pagar   = Sum(Case(When(tipo=TipoMovimentacaoChoices.DESPESA, status=StatusMovimentacaoChoices.PENDENTE, then='valor'), default=0, output_field=DecimalField()))
        )

        receitas_pagas = totais['receitas_pagas'] or Decimal('0')
        despesas_pagas = totais['despesas_pagas'] or Decimal('0')
        contas_receber = totais['contas_receber'] or Decimal('0')
        contas_pagar   = totais['contas_pagar'] or Decimal('0')
        saldo_atual    = receitas_pagas - despesas_pagas

        return Response({
            'receitas_pagas': float(receitas_pagas),
            'despesas_pagas': float(despesas_pagas),
            'saldo_atual'   : float(saldo_atual),
            'contas_receber': float(contas_receber),
            'contas_pagar'  : float(contas_pagar),
        })