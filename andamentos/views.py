from rest_framework                import viewsets, filters
from rest_framework.permissions    import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters                import rest_framework as django_filters
from .models                       import AndamentoProcessual, TipoEventoChoices
from .serializers                  import AndamentoProcessualSerializer


class AndamentoProcessualFilter(django_filters.FilterSet):
    publicado_para_cliente = django_filters.BooleanFilter()
    tipo_evento            = django_filters.ChoiceFilter(choices=TipoEventoChoices.choices)
    processo               = django_filters.NumberFilter(field_name='processo__id')
    cliente                = django_filters.NumberFilter(field_name='processo__cliente__id')
    created_after          = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    data_evento_after      = django_filters.DateTimeFilter(field_name='data_evento', lookup_expr='gte')
    data_evento_before     = django_filters.DateTimeFilter(field_name='data_evento', lookup_expr='lte')

    class Meta:
        model  = AndamentoProcessual
        fields = [
            'publicado_para_cliente', 
            'tipo_evento',
            'processo',
            'cliente',
            'created_after',
            'data_evento_after',
            'data_evento_before'
        ]


class AndamentoProcessualViewSet(viewsets.ModelViewSet):
    queryset           = AndamentoProcessual.objects.ativos().select_related('processo', 'processo__cliente')
    serializer_class   = AndamentoProcessualSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class    = AndamentoProcessualFilter
    search_fields      = ['processo__numero_processo', 'titulo', 'descricao']
    ordering_fields    = ['data_evento', 'created_at', 'updated_at']
    ordering           = ['-data_evento']