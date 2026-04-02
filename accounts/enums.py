from django.db import models
from django.utils.translation import gettext_lazy as _

class Sexo(models.TextChoices):
    MASCULINO = 'masculino', _('Masculino')
    FEMININO = 'feminino', _('Feminino')
    NAO_INFORMAR = 'nao_informar', _('Não Informar')

class EstadoCivil(models.TextChoices):
    SOLTEIRO = 'solteiro', _('Solteiro(a)')
    CASADO = 'casado', _('Casado(a)')
    DIVORCIADO = 'divorciado', _('Divorciado(a)')
    VIUVO = 'viuvo', _('Viúvo(a)')

class NivelProfissional(models.TextChoices):
    ESTAGIARIO = 'estagiario', _('Estagiário(a)')
    JUNIOR = 'junior', _('Júnior')
    PLENO = 'pleno', _('Pleno')
    SENIOR = 'senior', _('Sênior')
    SOCIO = 'socio', _('Sócio(a)')

class TipoContrato(models.TextChoices):
    CLT = 'clt', _('CLT')
    PJ = 'pj', _('Pessoa Jurídica')
    ASSOCIADO = 'associado', _('Associado')
    FREELANCER = 'freelancer', _('Freelancer')

class TipoConta(models.TextChoices):
    CORRENTE = 'corrente', _('Conta Corrente')
    POUPANCA = 'poupanca', _('Poupança')

class PreferenciasComunicacao(models.TextChoices):
    WHATSAPP = 'whatsapp', _('WhatsApp')
    EMAIL = 'email', _('E-mail')
    SISTEMA = 'sistema', _('Sistema Interno')