from django.contrib import admin
from .models import AndamentoProcessual


@admin.register(AndamentoProcessual)
class AndamentoProcessualAdmin(admin.ModelAdmin):
    list_display = [
        'processo', 'tipo_evento', 'titulo', 'data_evento', 
        'prazo_limite', 'publicado_para_cliente', 'created_at'
    ]
    list_filter = ['tipo_evento', 'publicado_para_cliente', 'data_evento', 'created_at']
    search_fields = ['processo__numero_processo', 'titulo', 'descricao']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'data_evento'
    
    fieldsets = (
        ('Informações do Andamento', {
            'fields': ('processo', 'tipo_evento', 'titulo', 'descricao')
        }),
        ('Datas', {
            'fields': ('data_evento', 'prazo_limite')
        }),
        ('Publicação', {
            'fields': ('publicado_para_cliente', 'canal_enviado')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
