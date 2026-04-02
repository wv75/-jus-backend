from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from processos.models import Processo
from clientes.models import Cliente


class NotificationLog(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('erro', 'Erro'),
        ('reagendado', 'Reagendado'),
    ]
    
    CANAL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]
    
    processo = models.ForeignKey(
        Processo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='notifications',
        verbose_name='Processo'
    )
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='notifications',
        verbose_name='Cliente'
    )
    evento = models.CharField(max_length=50, verbose_name='Evento')
    canal = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES,
        verbose_name='Canal'
    )
    payload_enviado = models.JSONField(
        default=dict, 
        blank=True,
        verbose_name='Payload Enviado',
        help_text='Dados enviados para o provedor'
    )
    resposta_provedor = models.JSONField(
        default=dict, 
        blank=True,
        verbose_name='Resposta do Provedor',
        help_text='Resposta recebida do provedor'
    )
    status_envio = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='pendente',
        verbose_name='Status do Envio'
    )
    tentativas = models.IntegerField(default=0, verbose_name='Tentativas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Log de Notificação'
        verbose_name_plural = 'Logs de Notificação'
        ordering = ['-created_at']

    def __str__(self):
        cliente_nome = self.cliente.nome if self.cliente else 'N/A'
        return f"{self.evento} - {cliente_nome} ({self.get_canal_display()})"


class Notification(models.Model):
    """
    Sistema de notificações internas para usuários do sistema
    """
    TIPO_CHOICES = [
        ('info', 'Informação'),
        ('warning', 'Aviso'),
        ('error', 'Erro'),
        ('success', 'Sucesso'),
        ('prazo', 'Prazo'),
        ('financeiro', 'Financeiro'),
        ('processo', 'Processo'),
        ('cliente', 'Cliente'),
        ('documento', 'Documento'),
        ('agenda', 'Agenda'),
    ]
    
    MODULO_CHOICES = [
        ('sistema', 'Sistema'),
        ('processos', 'Processos'),
        ('clientes', 'Clientes'),
        ('financeiro', 'Financeiro'),
        ('agenda', 'Agenda'),
        ('documentos', 'Documentos'),
        ('notifications', 'Notificações'),
    ]
    
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('lida', 'Lida'),
        ('arquivada', 'Arquivada'),
        ('expirada', 'Expirada'),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Destinatário'
    )
    
    # Conteúdo da notificação
    verb = models.CharField(max_length=100, verbose_name='Ação')
    description = models.TextField(blank=True, verbose_name='Descrição')
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_CHOICES,
        default='info',
        verbose_name='Tipo'
    )
    
    # Módulo e status (NOVOS CAMPOS)
    modulo = models.CharField(
        max_length=20,
        choices=MODULO_CHOICES,
        default='sistema',
        verbose_name='Módulo'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='ativa',
        verbose_name='Status'
    )
    
    # Relacionamentos opcionais
    processo = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Processo Relacionado'
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Cliente Relacionado'
    )
    
    # Status e controle
    unread = models.BooleanField(default=True, verbose_name='Não Lida')
    public = models.BooleanField(default=True, verbose_name='Pública')
    deleted = models.BooleanField(default=False, verbose_name='Deletada')
    
    # Timestamps
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Data/Hora')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Dados adicionais (JSON)
    data = models.JSONField(default=dict, blank=True, verbose_name='Dados Extras')

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient', 'unread']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.recipient.username} - {self.verb}"

    def mark_as_read(self):
        """Marca a notificação como lida"""
        if self.unread:
            self.unread = False
            self.save(update_fields=['unread'])

    def mark_as_unread(self):
        """Marca a notificação como não lida"""
        if not self.unread:
            self.unread = True
            self.save(update_fields=['unread'])

    @property
    def timesince(self):
        """Retorna tempo desde a criação"""
        from django.utils.timesince import timesince
        return timesince(self.timestamp)

    @classmethod
    def create_notification(cls, recipient, verb, description='', tipo='info', 
                          modulo='sistema', processo=None, cliente=None, data=None):
        """
        Método helper para criar notificações
        """
        return cls.objects.create(
            recipient=recipient,
            verb=verb,
            description=description,
            tipo=tipo,
            modulo=modulo,
            status='ativa',
            processo=processo,
            cliente=cliente,
            data=data or {}
        )

    @classmethod
    def notify_prazo_vencendo(cls, processo, dias_restantes):
        """Criar notificação para prazo vencendo"""
        users = User.objects.filter(is_active=True)
        for user in users:
            cls.create_notification(
                recipient=user,
                verb=f"Prazo vencendo em {dias_restantes} dias",
                description=f"O processo {processo.numero_processo} tem prazo em {processo.prazo_final.strftime('%d/%m/%Y')}",
                tipo='prazo',
                modulo='processos',
                processo=processo,
                cliente=processo.cliente,
                data={'dias_restantes': dias_restantes}
            )

    @classmethod
    def notify_conta_vencida(cls, movimentacao):
        """Criar notificação para conta vencida"""
        users = User.objects.filter(is_active=True)
        for user in users:
            cls.create_notification(
                recipient=user,
                verb="Conta vencida",
                description=f"{movimentacao.descricao} - R$ {movimentacao.valor} venceu em {movimentacao.data_vencimento.strftime('%d/%m/%Y')}",
                tipo='financeiro',
                modulo='financeiro',
                cliente=movimentacao.cliente,
                data={'valor': float(movimentacao.valor)}
            )

    @classmethod
    def notify_novo_processo(cls, processo):
        """Criar notificação para novo processo"""
        users = User.objects.filter(is_active=True)
        for user in users:
            cls.create_notification(
                recipient=user,
                verb="Novo processo criado",
                description=f"Processo {processo.numero_processo} criado para {processo.cliente.nome}",
                tipo='processo',
                modulo='processos',
                processo=processo,
                cliente=processo.cliente
            )

    @classmethod
    def notify_honorario_pendente(cls, honorario):
        """Criar notificação para honorário pendente de aprovação"""
        users = User.objects.filter(is_active=True)
        for user in users:
            cls.create_notification(
                recipient=user,
                verb="Honorário pendente de aprovação",
                description=f"Honorário de R$ {honorario.valor} para {honorario.cliente.nome} aguarda aprovação",
                tipo='financeiro',
                modulo='financeiro',
                cliente=honorario.cliente,
                data={'valor': float(honorario.valor)}
            )
    
    @classmethod
    def notify_novo_documento(cls, documento):
        """Criar notificação para novo documento"""
        users = User.objects.filter(is_active=True)
        for user in users:
            cls.create_notification(
                recipient=user,
                verb="Novo documento criado",
                description=f"Documento {documento.titulo} criado para {documento.cliente.nome}",
                tipo='documento',
                modulo='documentos',
                cliente=documento.cliente
            )
    
    @classmethod
    def notify_compromisso_automatico(cls, compromisso):
        """Criar notificação para compromisso criado automaticamente"""
        users = User.objects.filter(is_active=True)
        for user in users:
            cls.create_notification(
                recipient=user,
                verb="Compromisso criado automaticamente",
                description=f"Compromisso '{compromisso.titulo}' agendado para {compromisso.data_inicio.strftime('%d/%m/%Y %H:%M')}",
                tipo='agenda',
                modulo='agenda'
            )
