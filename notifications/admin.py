from django.contrib import admin
from .models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        'cliente', 'processo', 'evento', 'canal', 
        'status_envio', 'tentativas', 'created_at'
    ]
    list_filter = ['canal', 'status_envio', 'evento', 'created_at']
    search_fields = ['cliente__nome', 'processo__numero_processo', 'evento']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informações', {
            'fields': ('cliente', 'processo', 'evento', 'canal')
        }),
        ('Status', {
            'fields': ('status_envio', 'tentativas')
        }),
        ('Dados Técnicos', {
            'fields': ('payload_enviado', 'resposta_provedor'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
