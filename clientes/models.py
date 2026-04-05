from django.db                      import models
from django.contrib.auth.models     import User
from django.contrib.postgres.fields import ArrayField
from accounts.models                import Advogado


class BaseModel(models.Model):
    ativo      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    def ativos(self):
        return self.filter(ativo=True)


class CanalPreferidoChoices(models.TextChoices):
    WHATSAPP = 'WHATSAPP', 'WhatsApp'
    EMAIL    = 'EMAIL', 'Email'
    SMS      = 'SMS', 'SMS'


class EstadoCivilChoices(models.TextChoices):
    SOLTEIRO   = 'SOLTEIRO', 'Solteiro(a)'
    CASADO     = 'CASADO', 'Casado(a)'
    DIVORCIADO = 'DIVORCIADO', 'Divorciado(a)'
    VIUVO      = 'VIUVO', 'Viúvo(a)'
    UNIAO      = 'UNIAO', 'União Estável'


class TipoClienteChoices(models.TextChoices):
    PF = 'PF', 'Pessoa Física'
    PJ = 'PJ', 'Pessoa Jurídica'


class EnderecoMixin(models.Model):
    cep        = models.CharField(max_length=9, blank=True, default="")
    logradouro = models.CharField(max_length=200, blank=True, default="")
    numero     = models.CharField(max_length=20, blank=True, default="")
    bairro     = models.CharField(max_length=100, blank=True, default="")
    cidade     = models.CharField(max_length=100, blank=True, default="")
    estado     = models.CharField(max_length=2, blank=True, default="")

    class Meta:
        abstract = True


class Cliente(BaseModel):
    tipo               = models.CharField(max_length=2, choices=TipoClienteChoices.choices, default=TipoClienteChoices.PF)
    canal_preferido    = models.CharField(max_length=10, choices=CanalPreferidoChoices.choices, default=CanalPreferidoChoices.WHATSAPP)
    consentimento_lgpd = models.BooleanField(default=False)
    data_consentimento = models.DateTimeField(null=True, blank=True)
    advogado           = models.ForeignKey(Advogado, on_delete=models.PROTECT, null=True, blank=True)
    tipos_documento    = ArrayField(base_field=models.CharField(max_length=40), default=list, blank=True)
    usuarios           = models.ManyToManyField(User, blank=True)
    objects            = ActiveManager()

    class Meta:
        db_table            = 'clientes_cliente'
        verbose_name        = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering            = ['-created_at']
        indexes             = [
            models.Index(fields=['ativo', 'tipo']),
        ]

    def __str__(self):
        return f"Cliente ID: {self.id} ({self.tipo})"


class PessoaFisica(EnderecoMixin, BaseModel):
    cliente       = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='pf')
    nome_completo = models.CharField(max_length=200)
    cpf           = models.CharField(max_length=14, unique=True)
    telefone      = models.CharField(max_length=20, blank=True, default="")
    email         = models.EmailField(blank=True, default="")
    estado_civil  = models.CharField(max_length=20, choices=EstadoCivilChoices.choices, blank=True, default="")
    profissao     = models.CharField(max_length=100, blank=True, default="")
    nacionalidade = models.CharField(max_length=100, blank=True, default="")
    rne           = models.CharField(max_length=50, blank=True, default="")
    nome_mae      = models.CharField(max_length=200, blank=True, default="")
    nome_pai      = models.CharField(max_length=200, blank=True, default="")
    objects       = ActiveManager()

    class Meta:
        db_table            = 'clientes_pessoa_fisica'
        verbose_name        = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'

    def __str__(self):
        return self.nome_completo


class PessoaJuridica(EnderecoMixin, BaseModel):
    cliente       = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='pj')
    razao_social  = models.CharField(max_length=200)
    cnpj          = models.CharField(max_length=18, unique=True)
    representante = models.ForeignKey(PessoaFisica, on_delete=models.PROTECT, related_name='empresas_representadas')
    objects       = ActiveManager()

    class Meta:
        db_table            = 'clientes_pessoa_juridica'
        verbose_name        = 'Pessoa Jurídica'
        verbose_name_plural = 'Pessoas Jurídicas'

    def __str__(self):
        return self.razao_social