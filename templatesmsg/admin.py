from django.contrib import admin
from .models import TemplateMensagem


@admin.register(TemplateMensagem)
class TemplateMensagemAdmin(admin.ModelAdmin):
    list_display = ['canal', 'evento', 'linguagem', 'ativo', 'created_at']
    list_filter = ['canal', 'evento', 'linguagem', 'ativo', 'created_at']
    search_fields = ['conteudo']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Configuração', {
            'fields': ('canal', 'evento', 'linguagem', 'ativo')
        }),
        ('Conteúdo', {
            'fields': ('conteudo',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
