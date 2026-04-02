from django.contrib import admin
from .models import Processo


@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = [
        'numero_processo', 'cliente', 'foro', 'vara', 
        'advogado_responsavel', 'risco', 'prioridade', 'ativo', 'created_at'
    ]
    list_filter = ['risco', 'prioridade', 'ativo', 'foro', 'vara', 'created_at']
    search_fields = ['numero_processo', 'cliente__nome', 'assunto', 'parte_contraria']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações do Processo', {
            'fields': ('numero_processo', 'cliente', 'foro', 'vara', 'classe')
        }),
        ('Detalhes', {
            'fields': ('assunto', 'parte_contraria', 'situacao_atual')
        }),
        ('Gestão', {
            'fields': ('advogado_responsavel', 'risco', 'prioridade', 'ativo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
