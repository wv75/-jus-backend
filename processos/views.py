from rest_framework                import viewsets, filters, status
from rest_framework.permissions    import IsAuthenticated
from rest_framework.decorators     import action
from rest_framework.response       import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters                import rest_framework as django_filters
from django.shortcuts              import get_object_or_404

from .models                       import Processo, RiscoChoices, PrioridadeChoices, StatusProcessoChoices
from .serializers                  import ProcessoSerializer, ProcessoDetailSerializer, ProcessoListSerializer
from andamentos.models             import AndamentoProcessual, TipoEventoChoices


class ProcessoFilter(django_filters.FilterSet):
    ativo                = django_filters.BooleanFilter()
    risco                = django_filters.ChoiceFilter(choices=RiscoChoices.choices)
    prioridade           = django_filters.ChoiceFilter(choices=PrioridadeChoices.choices)
    status               = django_filters.ChoiceFilter(choices=StatusProcessoChoices.choices)
    cliente              = django_filters.NumberFilter(field_name='cliente__id')
    advogado_responsavel = django_filters.NumberFilter(field_name='advogado_responsavel__id')

    class Meta:
        model  = Processo
        fields = ['ativo', 'risco', 'prioridade', 'status', 'foro', 'vara']


class ProcessoViewSet(viewsets.ModelViewSet):
    queryset           = Processo.objects.ativos().select_related('cliente', 'advogado_responsavel')
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class    = ProcessoFilter
    search_fields      = ['numero_processo', 'cliente__nome', 'assunto', 'parte_contraria']
    ordering_fields    = ['numero_processo', 'created_at', 'updated_at']
    ordering           = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProcessoListSerializer
        if self.action == 'retrieve':
            return ProcessoDetailSerializer
        return ProcessoSerializer

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        processo   = self.get_object()
        new_status = request.data.get('status')

        if not new_status or new_status not in StatusProcessoChoices.values:
            return Response({'error': 'Status inválido ou não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)

        old_status = processo.status
        if old_status != new_status:
            processo.status = new_status
            processo.save()

            AndamentoProcessual.objects.create(
                processo               = processo,
                tipo_evento            = TipoEventoChoices.ANDAMENTO_GERAL,
                titulo                 = f'Status alterado para {processo.get_status_display()}',
                descricao              = f'Status do processo alterado de "{dict(StatusProcessoChoices.choices)[old_status]}" para "{dict(StatusProcessoChoices.choices)[new_status]}"',
                publicado_para_cliente = False 
            )

        serializer = ProcessoSerializer(processo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        processo = get_object_or_404(Processo.objects.all(), pk=pk)
        
        is_active      = request.data.get('ativo', not processo.ativo)
        processo.ativo = is_active
        processo.save()
        
        serializer = ProcessoSerializer(processo)
        return Response(serializer.data, status=status.HTTP_200_OK)