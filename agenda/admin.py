from django.contrib import admin
from .models import TipoCompromisso, Compromisso

@admin.register(TipoCompromisso)
class TipoCompromissoAdmin(admin.ModelAdmin):
    list_display = ["nome", "cor", "ativo"]
    list_filter = ["ativo"]
    search_fields = ["nome"]

@admin.register(Compromisso)  
class CompromissoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "data_inicio", "tipo", "prioridade", "responsavel", "concluido"]
    list_filter = ["tipo", "prioridade", "concluido", "data_inicio"]
    search_fields = ["titulo", "descricao"]
    date_hierarchy = "data_inicio"
