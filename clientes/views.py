from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters

from .models import Cliente
from .serializers import ClienteSerializer


class ClienteFilter(django_filters.FilterSet):
    """Filtros avançados para a listagem de clientes."""
    ativo = django_filters.BooleanFilter()
    consentimento_lgpd = django_filters.BooleanFilter()
    canal_preferido = django_filters.ChoiceFilter(choices=Cliente.CANAL_CHOICES)
    updated_after = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    
    class Meta:
        model = Cliente
        fields = ['ativo', 'consentimento_lgpd', 'canal_preferido']


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar clientes.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ClienteFilter
    search_fields = ['nome', 'documento', 'email', 'telefone_whatsapp']
    ordering_fields = ['nome', 'created_at', 'updated_at']
    
    # CORREÇÃO: O nome do campo no modelo usa underscore (_).
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        Ação para ativar ou desativar um cliente.
        URL: POST /api/v1/clientes/{pk}/toggle_status/
        """
        cliente = self.get_object()
        
        # Se 'ativo' não for passado no body, inverte o valor atual
        is_active = request.data.get('ativo', not cliente.ativo)

        cliente.ativo = is_active
        cliente.save()

        serializer = self.get_serializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)