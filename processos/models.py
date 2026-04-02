from django.db                  import models
from django.contrib.auth.models import User
from django.utils               import timezone
from clientes.models            import Cliente


class BaseModel(models.Model):
    ativo      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    def ativos(self):
        return self.filter(ativo=True)


class RiscoChoices(models.TextChoices):
    BAIXO = 'BAIXO', 'Baixo'
    MEDIO = 'MEDIO', 'Médio'
    ALTO  = 'ALTO', 'Alto'


class PrioridadeChoices(models.TextChoices):
    BAIXA = 'BAIXA', 'Baixa'
    MEDIA = 'MEDIA', 'Média'
    ALTA  = 'ALTA', 'Alta'


class StatusProcessoChoices(models.TextChoices):
    NOVO         = 'NOVO', 'Novo'
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em Andamento'
    SUSPENSO     = 'SUSPENSO', 'Suspenso'
    CONCLUIDO    = 'CONCLUIDO', 'Concluído'
    ARQUIVADO    = 'ARQUIVADO', 'Arquivado'


class Processo(BaseModel):
    numero_processo      = models.CharField(max_length=50, unique=True)
    cliente              = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='processos')
    tarefa               = models.CharField(max_length=200, blank=True, default="")
    foro                 = models.CharField(max_length=200, blank=True, default='padrao')
    vara                 = models.CharField(max_length=200, blank=True, default='padrao')
    comarca              = models.CharField(max_length=200, blank=True, default='padrao')
    classe               = models.CharField(max_length=200, blank=True, default='padrao')
    assunto              = models.CharField(max_length=500, blank=True, default='padrao')
    parte_contraria      = models.CharField(max_length=200, blank=True, default='padrao')
    situacao_atual       = models.CharField(max_length=200, blank=True, default="")
    status               = models.CharField(max_length=20, choices=StatusProcessoChoices.choices, default=StatusProcessoChoices.NOVO)
    risco                = models.CharField(max_length=10, choices=RiscoChoices.choices, default=RiscoChoices.MEDIO)
    prioridade           = models.CharField(max_length=10, choices=PrioridadeChoices.choices, default=PrioridadeChoices.MEDIA)
    prazo_final          = models.DateTimeField(null=True, blank=True)
    advogado_responsavel = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='processos_responsavel')
    objects              = ActiveManager()

    class Meta:
        db_table            = 'processos'
        verbose_name        = 'Processo'
        verbose_name_plural = 'Processos'
        ordering            = ['-created_at']
        indexes             = [
            models.Index(fields=['numero_processo']),
            models.Index(fields=['cliente', 'ativo']),
            models.Index(fields=['status', 'prazo_final']),
        ]

    def __str__(self):
        return f"{self.numero_processo} - {self.cliente_id}"

    @property
    def dias_para_prazo(self):
        if not self.prazo_final:
            return None
        delta = self.prazo_final - timezone.now()
        return delta.days

    @property
    def prazo_vencido(self):
        if not self.prazo_final:
            return False
        return self.prazo_final < timezone.now()

    @property
    def prazo_critico(self):
        dias = self.dias_para_prazo
        return dias is not None and 0 <= dias <= 7