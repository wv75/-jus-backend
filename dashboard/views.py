from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Importe os modelos de todos os apps que você precisa para os cálculos
from clientes.models import Cliente
from processos.models import Processo
from financeiro.models import MovimentacaoFinanceira, Honorario
from agenda.models import Compromisso
from notifications.models import Notification

# Importe os serializers para converter os dados para JSON (boa prática)
from financeiro.serializers import MovimentacaoFinanceiraSerializer
from processos.serializers import ProcessoSerializer # Use o serializer apropriado
from agenda.serializers import CompromissoSerializer
from notifications.serializers import NotificationSerializer


class DashboardExecutivoAPIView(APIView):
    """
    Endpoint de API que retorna todos os dados consolidados para o Dashboard Executivo.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        hoje = timezone.now().date()
        inicio_mes = hoje.replace(day=1)
        fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # KPIs Financeiros
        receitas_mes = MovimentacaoFinanceira.objects.filter(tipo='receita', data_pagamento__range=[inicio_mes, fim_mes], status='pago').aggregate(total=Sum('valor'))['total'] or Decimal('0')
        despesas_mes = MovimentacaoFinanceira.objects.filter(tipo='despesa', data_pagamento__range=[inicio_mes, fim_mes], status='pago').aggregate(total=Sum('valor'))['total'] or Decimal('0')
        contas_receber = MovimentacaoFinanceira.objects.filter(tipo='receita', status='pendente').aggregate(total=Sum('valor'))['total'] or Decimal('0')
        contas_pagar = MovimentacaoFinanceira.objects.filter(tipo='despesa', status='pendente').aggregate(total=Sum('valor'))['total'] or Decimal('0')
        
        # KPIs Operacionais
        total_clientes = Cliente.objects.filter(ativo=True).count()
        novos_clientes_mes = Cliente.objects.filter(created_at__range=[inicio_mes, fim_mes]).count()
        processos_ativos = Processo.objects.filter(ativo=True, status__in=['novo', 'em_andamento']).count()
        
        # Gráfico: Receitas vs Despesas (Últimos 6 meses)
        meses_dados, receitas_dados, despesas_dados = [], [], []
        for i in range(6):
            data_inicio = (hoje.replace(day=1) - timedelta(days=i*30)).replace(day=1)
            data_fim = (data_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            receita_mes = MovimentacaoFinanceira.objects.filter(tipo='receita', data_pagamento__range=[data_inicio, data_fim], status='pago').aggregate(total=Sum('valor'))['total'] or Decimal('0')
            despesa_mes = MovimentacaoFinanceira.objects.filter(tipo='despesa', data_pagamento__range=[data_inicio, data_fim], status='pago').aggregate(total=Sum('valor'))['total'] or Decimal('0')
            meses_dados.insert(0, data_inicio.strftime('%b/%Y'))
            receitas_dados.insert(0, float(receita_mes))
            despesas_dados.insert(0, float(despesa_mes))

        # Gráfico: Status dos processos
        status_processos = Processo.objects.filter(ativo=True).values('status').annotate(count=Count('id')).order_by('status')

        # Monta a resposta JSON
        data = {
            "kpis_financeiros": {
                "receitas_mes": receitas_mes,
                "despesas_mes": despesas_mes,
                "saldo_mes": receitas_mes - despesas_mes,
                "contas_receber": contas_receber,
                "contas_pagar": contas_pagar,
            },
            "kpis_operacionais": {
                "total_clientes": total_clientes,
                "novos_clientes_mes": novos_clientes_mes,
                "processos_ativos": processos_ativos,
            },
            "graficos": {
                "evolucao_financeira": {"labels": meses_dados, "receitas": receitas_dados, "despesas": despesas_dados},
                "status_processos": list(status_processos),
            }
        }
        return Response(data)


class DashboardOperacionalAPIView(APIView):
    """
    Endpoint de API que retorna dados para o Dashboard Operacional, focado no usuário logado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        hoje = timezone.now().date()
        semana = hoje + timedelta(days=7)
        user = request.user

        # Compromissos do usuário
        compromissos_hoje = Compromisso.objects.filter(data_inicio__date=hoje, responsavel=user).order_by('data_inicio')
        
        # Processos críticos
        processos_criticos = Processo.objects.filter(ativo=True, prazo_final__lte=semana, prazo_final__gte=hoje).order_by('prazo_final')
        
        # Notificações não lidas
        notificacoes_nao_lidas = Notification.objects.filter(recipient=user, unread=True).order_by('-timestamp')[:5]

        # Monta a resposta JSON
        data = {
            "compromissos_hoje": CompromissoSerializer(compromissos_hoje, many=True).data,
            "processos_criticos": ProcessoSerializer(processos_criticos, many=True).data,
            "notificacoes_nao_lidas": NotificationSerializer(notificacoes_nao_lidas, many=True).data,
            "atalhos_rapidos": {
                "compromissos_hoje_count": compromissos_hoje.count(),
                "processos_criticos_count": processos_criticos.count(),
            }
        }
        return Response(data)
