from django.db                  import models
from django.contrib.auth.models import User
from django.utils               import timezone
from decimal                    import Decimal


class BaseModel(models.Model):
    ativo      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    def ativos(self):
        return self.filter(ativo=True)


class TipoPlanoContaChoices(models.TextChoices):
    RECEITA    = 'RECEITA', 'Receita'
    DESPESA    = 'DESPESA', 'Despesa'
    ATIVO      = 'ATIVO', 'Ativo'
    PASSIVO    = 'PASSIVO', 'Passivo'
    PATRIMONIO = 'PATRIMONIO', 'Patrimônio'


class TipoMovimentacaoChoices(models.TextChoices):
    RECEITA       = 'RECEITA', 'Receita'
    DESPESA       = 'DESPESA', 'Despesa'
    TRANSFERENCIA = 'TRANSFERENCIA', 'Transferência'


class StatusMovimentacaoChoices(models.TextChoices):
    PENDENTE  = 'PENDENTE', 'Pendente'
    PAGO      = 'PAGO', 'Pago'
    CANCELADO = 'CANCELADO', 'Cancelado'


class ParcelamentoChoices(models.TextChoices):
    AVISTA = 'AVISTA', 'À Vista'
    X2     = '2X', '2x'
    X3     = '3X', '3x'
    X4     = '4X', '4x'
    X5     = '5X', '5x'
    X6     = '6X', '6x'
    X7     = '7X', '7x'
    X8     = '8X', '8x'
    X9     = '9X', '9x'
    X10    = '10X', '10x'
    X11    = '11X', '11x'
    X12    = '12X', '12x'
    X13    = '13X', '13x'
    X14    = '14X', '14x'
    X15    = '15X', '15x'
    X16    = '16X', '16x'
    X17    = '17X', '17x'
    X18    = '18X', '18x'
    X19    = '19X', '19x'
    X20    = '20X', '20x'
    X21    = '21X', '21x'
    X22    = '22X', '22x'
    X23    = '23X', '23x'
    X24    = '24X', '24x'


class TipoHonorarioChoices(models.TextChoices):
    FIXO       = 'FIXO', 'Valor Fixo'
    PERCENTUAL = 'PERCENTUAL', 'Percentual'
    HORA       = 'HORA', 'Por Hora'
    EXITO      = 'EXITO', 'Êxito'


class StatusHonorarioChoices(models.TextChoices):
    ORCAMENTO = 'ORCAMENTO', 'Orçamento'
    APROVADO  = 'APROVADO', 'Aprovado'
    FATURADO  = 'FATURADO', 'Faturado'
    PAGO      = 'PAGO', 'Pago'
    CANCELADO = 'CANCELADO', 'Cancelado'


class PlanoContas(BaseModel):
    codigo    = models.CharField(max_length=20, unique=True)
    nome      = models.CharField(max_length=200)
    tipo      = models.CharField(max_length=15, choices=TipoPlanoContaChoices.choices)
    conta_pai = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    objects   = ActiveManager()

    class Meta:
        db_table            = 'plano_contas'
        verbose_name        = 'Plano de Contas'
        verbose_name_plural = 'Plano de Contas'
        ordering            = ['codigo']
        indexes             = [
            models.Index(fields=['ativo', 'tipo']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class ContaBancaria(BaseModel):
    nome          = models.CharField(max_length=100)
    banco         = models.CharField(max_length=100)
    agencia       = models.CharField(max_length=20)
    conta         = models.CharField(max_length=20)
    saldo_inicial = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    objects       = ActiveManager()

    class Meta:
        db_table            = 'conta_bancaria'
        verbose_name        = 'Conta Bancária'
        verbose_name_plural = 'Contas Bancárias'
        ordering            = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.banco}"


class MovimentacaoFinanceira(BaseModel):
    tipo               = models.CharField(max_length=15, choices=TipoMovimentacaoChoices.choices)
    descricao          = models.CharField(max_length=200)
    valor              = models.DecimalField(max_digits=15, decimal_places=2)
    data_registro      = models.DateField(auto_now_add=True)
    data_vencimento    = models.DateField()
    data_pagamento     = models.DateField(null=True, blank=True)
    parcelamento       = models.CharField(max_length=20, choices=ParcelamentoChoices.choices, default=ParcelamentoChoices.AVISTA)
    vigencia_inicio    = models.DateField(null=True, blank=True)
    vigencia_fim       = models.DateField(null=True, blank=True)
    competencia_inicio = models.DateField(null=True, blank=True)
    competencia_fim    = models.DateField(null=True, blank=True)
    conta_bancaria     = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT)
    plano_conta        = models.ForeignKey(PlanoContas, on_delete=models.PROTECT)
    cliente            = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, null=True, blank=True)
    fornecedor         = models.ForeignKey('fornecedores.Fornecedor', on_delete=models.PROTECT, null=True, blank=True)
    processo           = models.ForeignKey('processos.Processo', on_delete=models.PROTECT, null=True, blank=True)
    status             = models.CharField(max_length=15, choices=StatusMovimentacaoChoices.choices, default=StatusMovimentacaoChoices.PENDENTE)
    observacoes        = models.TextField(blank=True, default="")
    comprovante        = models.FileField(upload_to='financeiro/comprovantes/', null=True, blank=True)
    responsavel        = models.ForeignKey(User, on_delete=models.PROTECT)
    numero_documento   = models.CharField(max_length=50, blank=True, default="")
    objects            = ActiveManager()

    class Meta:
        db_table            = 'movimentacao'
        verbose_name        = 'Movimentação Financeira'
        verbose_name_plural = 'Movimentações Financeiras'
        ordering            = ['-data_vencimento']
        indexes             = [
            models.Index(fields=['conta_bancaria', 'data_pagamento']),
            models.Index(fields=['status', 'data_vencimento']),
            models.Index(fields=['cliente', 'ativo']),
            models.Index(fields=['fornecedor', 'ativo']),
        ]

    def __str__(self):
        return f"{self.tipo} - {self.descricao} - R$ {self.valor}"


class Honorario(BaseModel):
    cliente           = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    processo          = models.ForeignKey('processos.Processo', on_delete=models.PROTECT, null=True, blank=True)
    descricao         = models.CharField(max_length=200)
    tipo              = models.CharField(max_length=15, choices=TipoHonorarioChoices.choices)
    valor             = models.DecimalField(max_digits=15, decimal_places=2)
    percentual        = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    valor_hora        = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    horas_trabalhadas = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    data_orcamento    = models.DateField(default=timezone.now)
    data_aprovacao    = models.DateField(null=True, blank=True)
    data_vencimento   = models.DateField()
    status            = models.CharField(max_length=15, choices=StatusHonorarioChoices.choices, default=StatusHonorarioChoices.ORCAMENTO)
    observacoes       = models.TextField(blank=True, default="")
    advogado          = models.ForeignKey(User, on_delete=models.PROTECT)
    numero_documento  = models.CharField(max_length=50, blank=True, default="")
    objects           = ActiveManager()

    class Meta:
        db_table            = 'honorario'
        verbose_name        = 'Honorário'
        verbose_name_plural = 'Honorários'
        ordering            = ['-created_at']
        indexes             = [
            models.Index(fields=['cliente', 'status']),
            models.Index(fields=['advogado', 'ativo']),
        ]

    def __str__(self):
        return f"{self.cliente_id} - {self.descricao} - R$ {self.valor}"

    def valor_total(self):
        if self.tipo == TipoHonorarioChoices.HORA and self.valor_hora and self.horas_trabalhadas:
            return self.valor_hora * self.horas_trabalhadas
        return self.valor