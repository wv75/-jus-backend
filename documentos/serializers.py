from rest_framework import serializers
from .models        import CategoriaDocumento, Documento, TemplateDocumento, AssinaturaDigital
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DocumentoUsuario


class CategoriaDocumentoSerializer(serializers.ModelSerializer):
    categoria_pai_nome = serializers.CharField(source='categoria_pai.nome', read_only=True)

    class Meta:
        model            = CategoriaDocumento
        fields           = [
            'id', 'ativo', 'nome', 'descricao', 'cor', 'icone', 
            'categoria_pai', 'categoria_pai_nome', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DocumentoSerializer(serializers.ModelSerializer):
    categoria_nome    = serializers.CharField(source='categoria.nome', read_only=True)
    cliente_nome      = serializers.CharField(source='cliente.nome', read_only=True)
    processo_numero   = serializers.CharField(source='processo.numero_processo', read_only=True)
    autor_nome        = serializers.CharField(source='autor.get_full_name', read_only=True)
    tipo_display      = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display    = serializers.CharField(source='get_status_display', read_only=True)
    tamanho_formatado = serializers.ReadOnlyField()
    extensao          = serializers.ReadOnlyField(source='extensao_arquivo')

    class Meta:
        model            = Documento
        fields           = [
            'id', 'ativo', 'titulo', 'descricao', 'tipo', 'tipo_display', 'categoria', 
            'categoria_nome', 'arquivo', 'tamanho_arquivo', 'tamanho_formatado', 
            'extensao', 'cliente', 'cliente_nome', 'processo', 'processo_numero', 
            'status', 'status_display', 'confidencialidade', 'versao', 'documento_pai', 
            'data_documento', 'data_vencimento', 'autor', 'autor_nome', 'revisor', 
            'palavras_chave', 'observacoes', 'publico', 'usuarios_acesso', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tamanho_arquivo']


class TemplateDocumentoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    autor_nome     = serializers.CharField(source='autor.get_full_name', read_only=True)
    tipo_display   = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model            = TemplateDocumento
        fields           = [
            'id', 'ativo', 'nome', 'descricao', 'tipo', 'tipo_display', 'categoria', 
            'categoria_nome', 'arquivo_template', 'variaveis', 'autor', 'autor_nome', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssinaturaDigitalSerializer(serializers.ModelSerializer):
    documento_titulo = serializers.CharField(source='documento.titulo', read_only=True)
    signatario_nome  = serializers.CharField(source='signatario.get_full_name', read_only=True)
    status_display   = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model            = AssinaturaDigital
        fields           = [
            'id', 'ativo', 'documento', 'documento_titulo', 'signatario', 'signatario_nome', 
            'status', 'status_display', 'data_solicitacao', 'data_assinatura', 
            'data_expiracao', 'ip_assinatura', 'certificado_digital', 'hash_assinatura', 
            'motivo_rejeicao', 'observacoes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'data_solicitacao', 'data_assinatura', 'created_at', 'updated_at']


User = get_user_model()

class DocumentoUsuarioSerializer(serializers.ModelSerializer):
    usuario      = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    arquivo_url  = serializers.SerializerMethodField()

    class Meta:
        model            = DocumentoUsuario
        fields           = [
            'id', 'usuario', 'usuario_nome', 'titulo', 'data_registro', 
            'descricao', 'arquivo', 'arquivo_url', 'ativo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_arquivo_url(self, obj):
        request = self.context.get('request')
        if obj.arquivo and hasattr(obj.arquivo, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.arquivo.url)
            return obj.arquivo.url
        return None