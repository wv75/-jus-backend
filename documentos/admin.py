from django.contrib import admin
from .models import CategoriaDocumento, Documento, TemplateDocumento, AssinaturaDigital, LogAcessoDocumento


@admin.register(CategoriaDocumento)
class CategoriaDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria_pai', 'ativo', 'created_at']
    list_filter = ['ativo', 'categoria_pai', 'created_at']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'categoria', 'cliente', 'processo', 'status', 'autor', 'created_at']
    list_filter = ['tipo', 'categoria', 'status', 'confidencialidade', 'publico', 'created_at']
    search_fields = ['titulo', 'descricao', 'palavras_chave']
    readonly_fields = ['tamanho_arquivo', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tipo', 'categoria')
        }),
        ('Arquivo', {
            'fields': ('arquivo', 'tamanho_arquivo')
        }),
        ('Relacionamentos', {
            'fields': ('cliente', 'processo')
        }),
        ('Status e Controle', {
            'fields': ('status', 'confidencialidade', 'versao', 'documento_pai')
        }),
        ('Datas', {
            'fields': ('data_documento', 'data_vencimento')
        }),
        ('Responsabilidades', {
            'fields': ('autor', 'revisor')
        }),
        ('Metadados', {
            'fields': ('palavras_chave', 'observacoes')
        }),
        ('Acesso', {
            'fields': ('publico', 'usuarios_acesso')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TemplateDocumento)
class TemplateDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'categoria', 'ativo', 'autor', 'created_at']
    list_filter = ['tipo', 'categoria', 'ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['tipo', 'nome']


@admin.register(AssinaturaDigital)
class AssinaturaDigitalAdmin(admin.ModelAdmin):
    list_display = ['documento', 'signatario', 'status', 'data_solicitacao', 'data_assinatura']
    list_filter = ['status', 'data_solicitacao', 'data_assinatura']
    search_fields = ['documento__titulo', 'signatario__username']
    readonly_fields = ['data_solicitacao', 'ip_assinatura', 'hash_assinatura']
    ordering = ['-data_solicitacao']


@admin.register(LogAcessoDocumento)
class LogAcessoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['documento', 'usuario', 'acao', 'sucesso', 'data_acesso']
    list_filter = ['acao', 'sucesso', 'data_acesso']
    search_fields = ['documento__titulo', 'usuario__username']
    readonly_fields = ['data_acesso']
    ordering = ['-data_acesso']
