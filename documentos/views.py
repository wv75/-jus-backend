from django.db.models              import Q
from django.shortcuts              import get_object_or_404
from rest_framework                import viewsets, filters, status
from rest_framework.permissions    import IsAuthenticated
from rest_framework.parsers        import MultiPartParser, FormParser
from rest_framework.decorators     import action
from rest_framework.response       import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models                       import CategoriaDocumento, Documento, TemplateDocumento, AssinaturaDigital, DocumentoUsuario
from .serializers                  import CategoriaDocumentoSerializer, DocumentoSerializer, TemplateDocumentoSerializer, AssinaturaDigitalSerializer, DocumentoUsuarioSerializer


class CategoriaDocumentoViewSet(viewsets.ModelViewSet):
    queryset           = CategoriaDocumento.objects.ativos()
    serializer_class   = CategoriaDocumentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['nome', 'descricao']
    ordering_fields    = ['nome', 'created_at']
    ordering           = ['nome']


class DocumentoViewSet(viewsets.ModelViewSet):
    serializer_class   = DocumentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['categoria', 'tipo', 'status', 'cliente', 'processo', 'autor']
    search_fields      = ['titulo', 'descricao', 'palavras_chave']
    ordering_fields    = ['titulo', 'data_documento', 'created_at']
    ordering           = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return Documento.objects.ativos().filter(
            Q(autor=user) |
            Q(publico=True) |
            Q(usuarios_acesso=user)
        ).distinct().select_related('categoria', 'cliente', 'processo', 'autor')

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class TemplateDocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = TemplateDocumento.objects.ativos().select_related('categoria', 'autor')
    serializer_class   = TemplateDocumentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['tipo', 'categoria']
    search_fields      = ['nome', 'descricao']
    ordering_fields    = ['nome', 'created_at']
    ordering           = ['tipo', 'nome']


class AssinaturaDigitalViewSet(viewsets.ModelViewSet):
    serializer_class   = AssinaturaDigitalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields   = ['status', 'documento']
    ordering_fields    = ['data_solicitacao', 'data_assinatura']
    ordering           = ['-data_solicitacao']

    def get_queryset(self):
        user = self.request.user
        return AssinaturaDigital.objects.ativos().filter(
            Q(signatario=user) |
            Q(documento__autor=user)
        ).distinct().select_related('documento', 'signatario')


class DocumentoUsuarioViewSet(viewsets.ModelViewSet):
    queryset           = DocumentoUsuario.objects.select_related('usuario').all()
    serializer_class   = DocumentoUsuarioSerializer
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['ativo', 'usuario']
    search_fields      = ['titulo', 'descricao', 'usuario__username', 'usuario__first_name']
    ordering_fields    = ['data_registro', 'created_at']
    ordering           = ['-data_registro']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(ativo=True)
        return queryset

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        documento       = get_object_or_404(DocumentoUsuario.objects.all(), pk=pk)
        is_active       = request.data.get('ativo', not documento.ativo)
        documento.ativo = is_active
        documento.save()
        
        serializer = self.get_serializer(documento)
        return Response(serializer.data, status=status.HTTP_200_OK)