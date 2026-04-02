from django.db                  import models
from django.contrib.auth.models import User
from django.utils               import timezone
from clientes.models            import Cliente

class CompromissoBase(models.Model):
    created_at  = models.DateTimeField( verbose_name='Criado em', 
                                        auto_now_add=True)
    updated_at  = models.DateTimeField(verbose_name='Atualizado em', 
                                       auto_now=True)
    
    class Meta:
        abstract            = True
        verbose_name        = "Tabela Base de Compromissos"
        db_table            = "compromisso_base"

class TipoCompromisso(CompromissoBase):
    nome    = models.CharField(max_length=100)
    cor     = models.CharField(max_length=7, default="#007bff")
    ativo   = models.BooleanField(default=True)
    
    class Meta:
        verbose_name        = "Tipo de Compromisso"
        verbose_name_plural = "Tipos de Compromissos"
        db_table            = "tipo_compromisso"
        ordering            = ["nome"]
    
    def __str__(self):
        return self.nome

class Compromisso(CompromissoBase):
    PRIORIDADE_CHOICES = [
        ("baixa", "Baixa"),
        ("media", "Média"), 
        ("alta", "Alta"),
        ("urgente", "Urgente"),
    ]
    tipo            = models.ForeignKey(TipoCompromisso, on_delete=models.CASCADE)
    titulo          = models.CharField(max_length=200)
    descricao       = models.TextField(blank=True)
    data_inicio     = models.DateTimeField()
    data_fim        = models.DateTimeField()
    tipo            = models.ForeignKey(TipoCompromisso, on_delete=models.CASCADE)
    prioridade      = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default="media")
    responsavel     = models.ForeignKey(User, on_delete=models.CASCADE)
    processo_relacionado = models.ForeignKey(
        'processos.Processo', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='Processo Relacionado'
    )
    concluido = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name        = "Compromisso"
        verbose_name_plural = "Compromissos"
        ordering            = ["-data_inicio"]
        db_table            = "compromisso"
    
    def __str__(self):
        return self.titulo


class ParticipantesCompromisso(CompromissoBase):

    compromisso = models.ForeignKey(Compromisso, on_delete=models.CASCADE, null=False, blank=False)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank= False)
    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)

    class Meta: 
        verbose_name    = "Participantes do Compromisso"
        ordering        = ["compromisso"]
        db_table        = "ParticipantesCompromisso"

    def __str__(self):
        return self.compromisso + self.user + self.cliente