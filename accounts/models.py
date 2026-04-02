from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from documentos.models import Documento, CategoriaDocumento 
from accounts.enums import Sexo, EstadoCivil, NivelProfissional, TipoContrato, TipoConta

class BaseModel(models.Model):
    ativo        = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    last_update  = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AdvogadoManager(models.Manager):
    def ativos(self):
        return self.filter(ativo=True)

class Advogado(BaseModel): 
    # ========== CAMPOS ==========
    id                     = models.AutoField(primary_key=True)
    nome                   = models.CharField(max_length=50)
    sobrenome              = models.CharField(max_length=100)
    cpf                    = models.CharField(max_length=14, unique=True, blank=True, default="")
    rg                     = models.CharField(max_length=20, blank=True, default="")
    data_nascimento        = models.DateField(null=True, blank=True)
    sexo                   = models.CharField(max_length=15, choices=Sexo, default='nao_informar')
    estado_civil           = models.CharField(max_length=15, choices=EstadoCivil, blank=True, default="")
    foto                   = models.ImageField(upload_to='advogados/fotos/', null=True, blank=True)
    telefone_celular       = models.CharField(max_length=20, blank=True, default="")
    telefone_fixo          = models.CharField(max_length=20, blank=True, default="")
    email                  = models.EmailField(max_length=100, unique=True, db_index=True)
    email_citacao          = models.EmailField(max_length=100, blank=True, default="")
    cep                    = models.CharField(max_length=10, blank=True, default="")
    logradouro             = models.CharField(max_length=100, blank=True, default="")
    numero                 = models.CharField(max_length=10, blank=True, default="")
    complemento            = models.CharField(max_length=50, blank=True, default="")
    bairro                 = models.CharField(max_length=50, blank=True, default="")
    cidade                 = models.CharField(max_length=50, blank=True, default="")
    uf                     = models.CharField(max_length=2, blank=True, default="")
    pais                   = models.CharField(max_length=50, default='Brasil')  
    oab_numero             = models.CharField(max_length=20, blank=True, default="")
    oab_uf                 = models.CharField(max_length=2, blank=True, default="")
    area_atuacao_principal = models.CharField(max_length=100, blank=True, default="")
    especialidades         = ArrayField(base_field=models.CharField(max_length=100), default=list, blank=True)
    descricao_profissional = models.TextField(blank=True, default="")
    nivel_profissional     = models.CharField(max_length=20, choices=NivelProfissional, default='junior')
    cargo                  = models.CharField(max_length=50, blank=True, default="")
    tipo_contrato          = models.CharField(max_length=20, choices=TipoContrato, blank=True, default="")
    valor_hora             = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pix_chave              = models.CharField(max_length=120, blank=True, default="")
    banco_nome             = models.CharField(max_length=50, blank=True, default="")
    agencia                = models.CharField(max_length=10, blank=True, default="")
    conta                  = models.CharField(max_length=20, blank=True, default="")
    tipo_conta             = models.CharField(max_length=20, choices=TipoConta, blank=True, default="")
    cpf_cnpj_conta         = models.CharField(max_length=20, blank=True, default="")
    
    documentos_pendentes   = models.BooleanField(default=False) 
    termo_assinado         = models.BooleanField(default=False)
    curriculo_pdf          = models.FileField(upload_to='advogados/curriculos/', null=True, blank=True)

    # ========== RELACIONAMENTOS ==========
    usuario                = models.OneToOneField(User, on_delete=models.PROTECT, related_name="perfil_advogado")
    supervisor             = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="supervisionados")
    documentos             = models.ManyToManyField(Documento, blank=True, related_name='advogados')
    criado_por             = models.ForeignKey(User, on_delete=models.PROTECT, related_name='advogados_criados')

    # ========== MANAGERS ==========
    objects                = AdvogadoManager()

    # ========== META ==========
    class Meta:
        ordering            = ['nome', 'sobrenome']
        verbose_name        = "Advogado"
        verbose_name_plural = "Advogados"
        db_table            = "advogado"
        
        # Regra 6: Integridade relacional no banco
        constraints = [
            models.UniqueConstraint(
                fields=["oab_numero", "oab_uf"],
                name="unique_advogado_oab",
                condition=~models.Q(oab_numero="") # Ignora se estiver vazio
            )
        ]
        
        # Regra 5: Índices para buscas frequentes
        indexes = [
            models.Index(fields=["ativo", "nivel_profissional"]),
        ]

    # ========== MÉTODOS ==========
    @property
    def full_name(self):
        return f"{self.nome} {self.sobrenome}".strip()

    def __str__(self):
        return self.full_name