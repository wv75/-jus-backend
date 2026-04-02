from django.db        import models
from processos.models import Processo


class BaseModel(models.Model):
    ativo      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AndamentoProcessualManager(models.Manager):
    def ativos(self):
        return self.filter(ativo=True)


class TipoEventoChoices(models.TextChoices):
    PETICAO              = 'PETICAO', 'Petição'
    AUDIENCIA_MARCADA    = 'AUDIENCIA_MARCADA', 'Audiência Marcada'
    SENTENCA_PUBLICADA   = 'SENTENCA_PUBLICADA', 'Sentença Publicada'
    DOCUMENTO_SOLICITADO = 'DOCUMENTO_SOLICITADO', 'Documento Solicitado'
    ANDAMENTO_GERAL      = 'ANDAMENTO_GERAL', 'Andamento Geral'


class AndamentoProcessual(BaseModel):
    processo               = models.ForeignKey(Processo, on_delete=models.PROTECT, related_name='andamentos')
    tipo_evento            = models.CharField(max_length=30, choices=TipoEventoChoices.choices, default=TipoEventoChoices.ANDAMENTO_GERAL)
    titulo                 = models.CharField(max_length=200)
    descricao              = models.TextField(blank=True, default="")
    data_evento            = models.DateTimeField()
    prazo_limite           = models.DateTimeField(null=True, blank=True)
    publicado_para_cliente = models.BooleanField(default=False)
    canal_enviado          = models.JSONField(default=dict, blank=True)
    objects                = AndamentoProcessualManager()

    class Meta:
        db_table            = 'processos_andamento_processual'
        verbose_name        = 'Andamento Processual'
        verbose_name_plural = 'Andamentos Processuais'
        ordering            = ['-data_evento']
        indexes             = [
            models.Index(fields=['processo', 'data_evento']),
            models.Index(fields=['ativo', 'tipo_evento']),
        ]

    def __str__(self):
        return f"{self.processo_id} - {self.titulo}"

    @property
    def data_evento_fmt(self):
        return self.data_evento.strftime('%d/%m/%Y às %H:%M')