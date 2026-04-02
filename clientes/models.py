from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from documentos.models import Documento, CategoriaDocumento
from accounts.models import Advogado

class Cliente(models.Model):
    CANAL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name='Nome')
    documento = models.CharField(max_length=20, unique=True, verbose_name='Documento')
    email = models.EmailField(verbose_name='Email')
    telefone_whatsapp = models.CharField(max_length=20, verbose_name='Telefone/WhatsApp')
    consentimento_lgpd = models.BooleanField(default=False, verbose_name='Consentimento LGPD')
    data_consentimento = models.DateTimeField(null=True, blank=True, verbose_name='Data do Consentimento')
    documento_pendente = models.BooleanField(default=False)
    advogado = models.ForeignKey(Advogado, on_delete=models.SET_NULL, null=True, blank=False)

    # Armazena as categorias escolhidas (nomes) no mesmo campo
    tipos_documento = ArrayField(
        base_field=models.CharField(max_length=40),
        default=list,
        blank=True,
        help_text="Categorias de documento associadas ao cliente"
    )
    canal_preferido = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='whatsapp',
        verbose_name='Canal Preferido'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    usuarios = models.ManyToManyField(
        User, 
        blank=True, 
        verbose_name='Usuários Vinculados',
        help_text='Usuários que têm acesso a este cliente'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.consentimento_lgpd and not self.data_consentimento:
            self.data_consentimento = timezone.now()
        super().save(*args, **kwargs)

    @property
    def primeiro_nome(self):
        return self.nome.split()[0] if self.nome else ''
