from rest_framework             import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators  import action
from rest_framework.response    import Response
from django.shortcuts           import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models      import PessoaFisica, PessoaJuridica
from .serializers import PessoaFisicaSerializer, PessoaJuridicaSerializer


class PessoaFisicaViewSet(viewsets.ModelViewSet):
    queryset           = PessoaFisica.objects.ativos().select_related('cliente')
    serializer_class   = PessoaFisicaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['ativo', 'cliente__consentimento_lgpd', 'cliente__canal_preferido']
    search_fields      = ['nome_completo', 'cpf', 'email', 'telefone']
    ordering_fields    = ['nome_completo', 'created_at']
    ordering           = ['nome_completo']

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        pf            = get_object_or_404(PessoaFisica.objects.all(), pk=pk)
        is_active     = request.data.get('ativo', not pf.ativo)
        pf.ativo      = is_active
        pf.save()
        
        pf.cliente.ativo = is_active
        pf.cliente.save()

        serializer = self.get_serializer(pf)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PessoaJuridicaViewSet(viewsets.ModelViewSet):
    queryset           = PessoaJuridica.objects.ativos().select_related('cliente', 'representante')
    serializer_class   = PessoaJuridicaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['ativo', 'cliente__consentimento_lgpd', 'cliente__canal_preferido']
    search_fields      = ['razao_social', 'cnpj', 'representante__nome_completo']
    ordering_fields    = ['razao_social', 'created_at']
    ordering           = ['razao_social']

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        pj            = get_object_or_404(PessoaJuridica.objects.all(), pk=pk)
        is_active     = request.data.get('ativo', not pj.ativo)
        pj.ativo      = is_active
        pj.save()
        
        pj.cliente.ativo = is_active
        pj.cliente.save()

        serializer = self.get_serializer(pj)
        return Response(serializer.data, status=status.HTTP_200_OK)