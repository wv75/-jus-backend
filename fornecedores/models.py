from django.db import models


class BaseModel(models.Model):
    ativo      = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    def ativos(self):
        return self.filter(ativo=True)


class Fornecedor(BaseModel):
    nome      = models.CharField(max_length=200)
    documento = models.CharField(max_length=50, blank=True, default="")
    contato   = models.CharField(max_length=100, blank=True, default="")
    objects   = ActiveManager()

    class Meta:
        db_table            = 'fornecedores'
        verbose_name        = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering            = ['nome']
        indexes             = [
            models.Index(fields=['ativo', 'nome']),
            models.Index(fields=['documento']),
        ]

    def __str__(self):
        return self.nome