from django.db                  import models
from django.contrib.auth.models import User
from django.utils               import timezone
from django.core.validators     import FileExtensionValidator
import os
from django.conf            import settings



def upload_documento_path(instance, filename):
    now    = timezone.now()
    folder = f"documentos/{now.year}/{now.month:02d}/geral"
    
    if instance.cliente_id:
        folder = f"documentos/{now.year}/{now.month:02d}/cliente_{instance.cliente_id}"
    elif instance.processo_id:
        folder = f"documentos/{now.year}/{now.month:02d}/processo_{instance.processo_id}"
        
    return f"{folder}/{filename}"


class BaseModel(models.Model):
    ativo      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    def ativos(self):
        return self.filter(ativo=True)


class TipoDocumentoChoices(models.TextChoices):
    PETICAO     = 'PETICAO', 'Petição'
    CONTRATO    = 'CONTRATO', 'Contrato'
    PROCURACAO  = 'PROCURACAO', 'Procuração'
    CERTIDAO    = 'CERTIDAO', 'Certidão'
    OFICIO      = 'OFICIO', 'Ofício'
    ATA         = 'ATA', 'Ata'
    PARECER     = 'PARECER', 'Parecer'
    RELATORIO   = 'RELATORIO', 'Relatório'
    COMPROVANTE = 'COMPROVANTE', 'Comprovante'
    OUTRO       = 'OUTRO', 'Outro'


class StatusDocumentoChoices(models.TextChoices):
    RASCUNHO  = 'RASCUNHO', 'Rascunho'
    REVISAO   = 'REVISAO', 'Em Revisão'
    APROVADO  = 'APROVADO', 'Aprovado'
    ASSINADO  = 'ASSINADO', 'Assinado'
    ENVIADO   = 'ENVIADO', 'Enviado'
    ARQUIVADO = 'ARQUIVADO', 'Arquivado'


class ConfidencialidadeChoices(models.TextChoices):
    PUBLICO      = 'PUBLICO', 'Público'
    INTERNO      = 'INTERNO', 'Interno'
    CONFIDENCIAL = 'CONFIDENCIAL', 'Confidencial'
    SECRETO      = 'SECRETO', 'Secreto'


class TipoTemplateChoices(models.TextChoices):
    PETICAO_INICIAL    = 'PETICAO_INICIAL', 'Petição Inicial'
    CONTESTACAO        = 'CONTESTACAO', 'Contestação'
    RECURSO            = 'RECURSO', 'Recurso'
    CONTRATO_PRESTACAO = 'CONTRATO_PRESTACAO', 'Contrato de Prestação de Serviços'
    PROCURACAO         = 'PROCURACAO', 'Procuração'
    OFICIO             = 'OFICIO', 'Ofício'
    ATA_REUNIAO        = 'ATA_REUNIAO', 'Ata de Reunião'
    PARECER_JURIDICO   = 'PARECER_JURIDICO', 'Parecer Jurídico'
    OUTRO              = 'OUTRO', 'Outro'


class StatusAssinaturaChoices(models.TextChoices):
    PENDENTE  = 'PENDENTE', 'Pendente'
    ASSINADO  = 'ASSINADO', 'Assinado'
    REJEITADO = 'REJEITADO', 'Rejeitado'
    EXPIRADO  = 'EXPIRADO', 'Expirado'


class AcaoLogChoices(models.TextChoices):
    VISUALIZAR   = 'VISUALIZAR', 'Visualizar'
    DOWNLOAD     = 'DOWNLOAD', 'Download'
    EDITAR       = 'EDITAR', 'Editar'
    COMPARTILHAR = 'COMPARTILHAR', 'Compartilhar'
    ASSINAR      = 'ASSINAR', 'Assinar'
    EXCLUIR      = 'EXCLUIR', 'Excluir'


class CategoriaDocumento(BaseModel):
    nome          = models.CharField(max_length=100)
    descricao     = models.TextField(blank=True, default="")
    cor           = models.CharField(max_length=7, default='#007bff')
    icone         = models.CharField(max_length=50, default='bi-file-text')
    categoria_pai = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    objects       = ActiveManager()

    class Meta:
        db_table            = 'categoria'
        verbose_name        = 'Categoria de Documento'
        verbose_name_plural = 'Categorias de Documentos'
        ordering            = ['nome']

    def __str__(self):
        return self.nome


class Documento(BaseModel):
    titulo            = models.CharField(max_length=200)
    descricao         = models.TextField(blank=True, default="")
    tipo              = models.CharField(max_length=20, choices=TipoDocumentoChoices.choices)
    categoria         = models.ForeignKey(CategoriaDocumento, on_delete=models.PROTECT)
    arquivo           = models.FileField(upload_to=upload_documento_path, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'])])
    tamanho_arquivo   = models.BigIntegerField(null=True, blank=True)
    cliente           = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, null=True, blank=True, related_name='documentos_cliente')
    processo          = models.ForeignKey('processos.Processo', on_delete=models.PROTECT, null=True, blank=True, related_name='documentos_processo')
    status            = models.CharField(max_length=15, choices=StatusDocumentoChoices.choices, default=StatusDocumentoChoices.RASCUNHO)
    confidencialidade = models.CharField(max_length=15, choices=ConfidencialidadeChoices.choices, default=ConfidencialidadeChoices.INTERNO)
    versao            = models.CharField(max_length=10, default='1.0')
    documento_pai     = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    data_documento    = models.DateField(default=timezone.now)
    data_vencimento   = models.DateField(null=True, blank=True)
    autor             = models.ForeignKey(User, on_delete=models.PROTECT, related_name='documentos_autor', default=1)
    revisor           = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_revisor')
    palavras_chave    = models.CharField(max_length=500, blank=True, default="")
    observacoes       = models.TextField(blank=True, default="")
    publico           = models.BooleanField(default=False)
    usuarios_acesso   = models.ManyToManyField(User, blank=True, related_name='documentos_acesso')
    objects           = ActiveManager()

    class Meta:
        db_table            = 'documento'
        verbose_name        = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering            = ['-created_at']
        indexes             = [
            models.Index(fields=['cliente', 'ativo']),
            models.Index(fields=['processo', 'ativo']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.titulo} (v{self.versao})"

    def save(self, *args, **kwargs):
        if self.arquivo:
            self.tamanho_arquivo = self.arquivo.size
        super().save(*args, **kwargs)

    def extensao_arquivo(self):
        if self.arquivo:
            return os.path.splitext(self.arquivo.name)[1].lower()
        return ''

    def tamanho_formatado(self):
        if not self.tamanho_arquivo:
            return '0 B'
        
        size = self.tamanho_arquivo
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def pode_acessar(self, usuario):
        if self.autor_id == usuario.id or self.publico:
            return True
        return self.usuarios_acesso.filter(id=usuario.id).exists()

    def pode_editar(self, usuario):
        return self.autor_id == usuario.id or self.revisor_id == usuario.id


class TemplateDocumento(BaseModel):
    nome             = models.CharField(max_length=100)
    descricao        = models.TextField(blank=True, default="")
    tipo             = models.CharField(max_length=30, choices=TipoTemplateChoices.choices)
    categoria        = models.ForeignKey(CategoriaDocumento, on_delete=models.PROTECT)
    arquivo_template = models.FileField(upload_to='templates/', validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'odt'])])
    variaveis        = models.JSONField(default=list)
    autor            = models.ForeignKey(User, on_delete=models.PROTECT)
    objects          = ActiveManager()

    class Meta:
        db_table            = 'template'
        verbose_name        = 'Template de Documento'
        verbose_name_plural = 'Templates de Documentos'
        ordering            = ['tipo', 'nome']

    def __str__(self):
        return self.nome


class AssinaturaDigital(BaseModel):
    documento           = models.ForeignKey(Documento, on_delete=models.PROTECT)
    signatario          = models.ForeignKey(User, on_delete=models.PROTECT)
    status              = models.CharField(max_length=15, choices=StatusAssinaturaChoices.choices, default=StatusAssinaturaChoices.PENDENTE)
    data_solicitacao    = models.DateTimeField(auto_now_add=True)
    data_assinatura     = models.DateTimeField(null=True, blank=True)
    data_expiracao      = models.DateTimeField(null=True, blank=True)
    ip_assinatura       = models.GenericIPAddressField(null=True, blank=True)
    certificado_digital = models.TextField(blank=True, default="")
    hash_assinatura     = models.CharField(max_length=128, blank=True, default="")
    motivo_rejeicao     = models.TextField(blank=True, default="")
    observacoes         = models.TextField(blank=True, default="")
    objects             = ActiveManager()

    class Meta:
        db_table            = 'assinatura_digital'
        verbose_name        = 'Assinatura Digital'
        verbose_name_plural = 'Assinaturas Digitais'
        ordering            = ['-data_solicitacao']
        constraints         = [
            models.UniqueConstraint(fields=['documento', 'signatario'], name='unique_documento_signatario')
        ]

    def __str__(self):
        return f"Doc: {self.documento_id} | Signatário: {self.signatario_id}"


class LogAcessoDocumento(BaseModel):
    documento   = models.ForeignKey(Documento, on_delete=models.PROTECT)
    usuario     = models.ForeignKey(User, on_delete=models.PROTECT)
    acao        = models.CharField(max_length=20, choices=AcaoLogChoices.choices)
    ip_address  = models.GenericIPAddressField()
    user_agent  = models.TextField(blank=True, default="")
    data_acesso = models.DateTimeField(auto_now_add=True)
    detalhes    = models.JSONField(default=dict)
    sucesso     = models.BooleanField(default=True)
    objects     = ActiveManager()

    class Meta:
        db_table            = 'log_acesso'
        verbose_name        = 'Log de Acesso a Documento'
        verbose_name_plural = 'Logs de Acesso a Documentos'
        ordering            = ['-data_acesso']

    def __str__(self):
        return f"Doc: {self.documento_id} | Usuário: {self.usuario_id} | Ação: {self.acao}"
    

class DocumentoUsuario(models.Model):
    usuario       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documentos')
    titulo        = models.CharField(max_length=255)
    data_registro = models.DateField(default=timezone.now)
    descricao     = models.TextField(blank=True, default="")
    arquivo       = models.FileField(
        upload_to='documentos/usuarios/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    ativo         = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table            = 'config_documento_usuario'
        verbose_name        = 'Documento de Usuário'
        verbose_name_plural = 'Documentos de Usuários'
        ordering            = ['-data_registro']
        indexes             = [
            models.Index(fields=['usuario', 'ativo']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.usuario_id}"