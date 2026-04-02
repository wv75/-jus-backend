from rest_framework                import viewsets, filters
from rest_framework.permissions    import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models                       import Fornecedor
from fornecedores.serializers      import FornecedorSerializer


class FornecedorViewSet(viewsets.ModelViewSet):
    queryset           = Fornecedor.objects.ativos()
    serializer_class   = FornecedorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['ativo']
    search_fields      = ['nome', 'documento', 'contato']
    ordering_fields    = ['nome', 'created_at']
    ordering           = ['nome']