from rest_framework                import viewsets, filters, generics, status
from rest_framework.permissions    import IsAuthenticated
from rest_framework.pagination     import PageNumberPagination
from rest_framework.views          import APIView
from rest_framework.response       import Response
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models                       import Advogado
from .serializers                  import AdvogadoSimpleSerializer, UserSerializer, AdvogadoCreateSerializer, AdvogadoListSerializer


class DefaultPagination(PageNumberPagination):
    page_size             = 25
    page_size_query_param = 'page_size'
    max_page_size         = 100

class DropdownPagination(PageNumberPagination):
    page_size             = 1000
    page_size_query_param = 'page_size'
    max_page_size         = 1000


class AdvogadoFilter(django_filters.FilterSet):
    ativo = django_filters.BooleanFilter()

    class Meta:
        model  = Advogado
        fields = ['ativo']


class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserManagementViewSet(viewsets.ModelViewSet):
    queryset           = Advogado.objects.select_related('usuario', 'supervisor', 'criado_por').all().order_by('nome')
    permission_classes = [IsAuthenticated]
    pagination_class   = DefaultPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class    = AdvogadoFilter
    search_fields      = ['nome', 'sobrenome', 'cargo', 'usuario__username', 'usuario__email']

    def get_serializer_class(self):
        if self.action == 'create':
            return AdvogadoCreateSerializer
        return AdvogadoListSerializer


class AdvogadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = Advogado.objects.ativos().select_related('usuario').order_by('nome')
    serializer_class   = AdvogadoSimpleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class   = DropdownPagination


class AdvogadoCreateView(generics.CreateAPIView):
    queryset           = Advogado.objects.all()
    serializer_class   = AdvogadoCreateSerializer
    permission_classes = [IsAuthenticated]