from rest_framework                 import viewsets
from rest_framework.decorators      import action
from rest_framework.response        import Response
from django_filters.rest_framework  import DjangoFilterBackend
from rest_framework.filters         import SearchFilter, OrderingFilter
from django.utils                   import timezone
from datetime                       import timedelta
from .models                        import TipoCompromisso, Compromisso
from .serializers                   import TipoCompromissoSerializer, CompromissoSerializer


class TipoCompromissoViewSet(viewsets.ModelViewSet):

    queryset = TipoCompromisso.objects.all()
    serializer_class = TipoCompromissoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ativo']
    search_fields = ['nome']
    ordering_fields = ['nome', 'ativo']
    ordering = ['nome']


class CompromissoViewSet(viewsets.ModelViewSet):

    queryset = Compromisso.objects.all()
    serializer_class = CompromissoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo', 'prioridade', 'responsavel', 'concluido']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_inicio', 'data_fim', 'titulo', 'prioridade']
    ordering = ['-data_inicio']

    def get_queryset(self):

        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(responsavel=user)
        return Compromisso.objects.none() 

    def perform_create(self, serializer):

        serializer.save(responsavel=self.request.user)

    @action(detail=False, methods=['get'])
    def hoje(self, request):

        hoje_data = timezone.now().date()
        compromissos = self.get_queryset().filter(
            data_inicio__date=hoje_data
        )
        serializer = self.get_serializer(compromissos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def proximos(self, request):

        hoje_data = timezone.now().date()
        proxima_semana = hoje_data + timedelta(days=7)
        
        compromissos = self.get_queryset().filter(
            data_inicio__date__range=[hoje_data, proxima_semana]
        )
        serializer = self.get_serializer(compromissos, many=True)
        return Response(serializer.data)