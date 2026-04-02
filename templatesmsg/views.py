from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters

from .models import TemplateMensagem
from .serializers import TemplateMensagemSerializer


class TemplateMensagemFilter(django_filters.FilterSet):
    """Filtros para os templates de mensagem."""
    ativo = django_filters.BooleanFilter()
    canal = django_filters.ChoiceFilter(choices=TemplateMensagem.CANAL_CHOICES)
    evento = django_filters.ChoiceFilter(choices=TemplateMensagem.EVENTO_CHOICES)
    linguagem = django_filters.CharFilter()
    
    class Meta:
        model = TemplateMensagem
        fields = ['ativo', 'canal', 'evento', 'linguagem']


class TemplateMensagemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar os templates de mensagem do sistema.
    """
    queryset = TemplateMensagem.objects.all()
    serializer_class = TemplateMensagemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TemplateMensagemFilter
    search_fields = ['conteudo', 'evento'] # Adicionado 'evento' ao campo de busca
    ordering_fields = ['canal', 'evento', 'created_at']
    ordering = ['canal', 'evento']
