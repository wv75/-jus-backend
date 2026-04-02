from django.db import models


class TemplateMensagem(models.Model):
    CANAL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]
    
    EVENTO_CHOICES = [
        ('peticao', 'Petição'),
        ('audiencia_marcada', 'Audiência Marcada'),
        ('sentenca_publicada', 'Sentença Publicada'),
        ('documento_solicitado', 'Documento Solicitado'),
        ('andamento_geral', 'Andamento Geral'),
        ('resumo_semanal', 'Resumo Semanal'),
    ]
    
    canal = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES,
        verbose_name='Canal'
    )
    evento = models.CharField(
        max_length=30, 
        choices=EVENTO_CHOICES,
        verbose_name='Evento'
    )
    linguagem = models.CharField(
        max_length=10, 
        default='pt-BR',
        verbose_name='Linguagem'
    )
    conteudo = models.TextField(
        verbose_name='Conteúdo',
        help_text='Use placeholders como {{primeiro_nome}}, {{numero_processo}}, {{data_evento_fmt}}'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Template de Mensagem'
        verbose_name_plural = 'Templates de Mensagem'
        unique_together = ['canal', 'evento', 'linguagem']
        ordering = ['canal', 'evento']

    def __str__(self):
        return f"{self.get_canal_display()} - {self.get_evento_display()}"
