from django.contrib import admin
from .models        import Cliente, PessoaFisica, PessoaJuridica


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'tipo', 'canal_preferido', 'consentimento_lgpd', 'ativo', 'created_at']
    list_filter   = ['tipo', 'ativo', 'consentimento_lgpd', 'canal_preferido']
    search_fields = ['id']


@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display  = ['nome_completo', 'cpf', 'email', 'telefone', 'ativo']
    list_filter   = ['ativo', 'estado_civil']
    search_fields = ['nome_completo', 'cpf', 'email']


@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display  = ['razao_social', 'cnpj', 'representante', 'ativo']
    list_filter   = ['ativo']
    search_fields = ['razao_social', 'cnpj', 'representante__nome_completo']