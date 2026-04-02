# accounts/admin.py
from django.contrib import admin
from .models import Advogado

@admin.register(Advogado)
class AdvogadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'ativo', 'email')
    list_filter = ('ativo',)
    search_fields = ('nome', 'sobrenome', 'email')