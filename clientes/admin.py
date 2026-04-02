from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'documento', 'email', 'telefone_whatsapp', 
        'canal_preferido', 'consentimento_lgpd', 'ativo', 'created_at'
    ]
    list_filter = ['canal_preferido', 'consentimento_lgpd', 'ativo', 'created_at']
    search_fields = ['nome', 'documento', 'email', 'telefone_whatsapp']
    readonly_fields = ['created_at', 'updated_at', 'data_consentimento']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'documento', 'email', 'telefone_whatsapp')
        }),
        ('Preferências', {
            'fields': ('canal_preferido', 'ativo')
        }),
        ('LGPD', {
            'fields': ('consentimento_lgpd', 'data_consentimento')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
