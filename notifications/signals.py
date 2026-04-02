from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from processos.models import Processo
from financeiro.models import MovimentacaoFinanceira, Honorario
from agenda.models import Compromisso
from .models import Notification


@receiver(post_save, sender=Processo)
def processo_created_notification(sender, instance, created, **kwargs):
    """
    Criar notificação quando um novo processo é criado
    """
    if created:
        Notification.notify_novo_processo(instance)


@receiver(post_save, sender=MovimentacaoFinanceira)
def movimentacao_financeira_notification(sender, instance, created, **kwargs):
    """
    Criar notificação para movimentações financeiras vencidas
    """
    hoje = timezone.now().date()
    
    # Verificar se a conta está vencida
    if (instance.status == 'pendente' and 
        instance.data_vencimento < hoje):
        Notification.notify_conta_vencida(instance)


@receiver(post_save, sender=Honorario)
def honorario_notification(sender, instance, created, **kwargs):
    """
    Criar notificação para honorários pendentes de aprovação
    """
    if created and instance.status == 'orcamento':
        Notification.notify_honorario_pendente(instance)


@receiver(post_save, sender=Compromisso)
def compromisso_created_notification(sender, instance, created, **kwargs):
    """
    Criar notificação quando um novo compromisso é criado
    """
    if created:
        from django.contrib.auth.models import User
        
        # Notificar o responsável
        Notification.create_notification(
            recipient=instance.responsavel,
            verb="Novo compromisso agendado",
            description=f"{instance.titulo} agendado para {instance.data_inicio.strftime('%d/%m/%Y às %H:%M')}",
            tipo='info',
            data={
                'compromisso_id': instance.id,
                'data_inicio': instance.data_inicio.isoformat()
            }
        )


# Signal personalizado para verificar prazos
def check_prazos_vencendo():
    """
    Função para verificar processos com prazos vencendo
    Esta função deve ser chamada por um cron job ou task scheduler
    """
    hoje = timezone.now().date()
    
    # Processos com prazo em 7 dias
    processos_7_dias = Processo.objects.filter(
        ativo=True,
        prazo_final=hoje + timedelta(days=7)
    )
    
    for processo in processos_7_dias:
        Notification.notify_prazo_vencendo(processo, 7)
    
    # Processos com prazo em 3 dias
    processos_3_dias = Processo.objects.filter(
        ativo=True,
        prazo_final=hoje + timedelta(days=3)
    )
    
    for processo in processos_3_dias:
        Notification.notify_prazo_vencendo(processo, 3)
    
    # Processos com prazo em 1 dia
    processos_1_dia = Processo.objects.filter(
        ativo=True,
        prazo_final=hoje + timedelta(days=1)
    )
    
    for processo in processos_1_dia:
        Notification.notify_prazo_vencendo(processo, 1)
    
    # Processos vencidos hoje
    processos_vencidos = Processo.objects.filter(
        ativo=True,
        prazo_final=hoje
    )
    
    for processo in processos_vencidos:
        Notification.notify_prazo_vencendo(processo, 0)


def check_contas_vencidas():
    """
    Função para verificar contas vencidas
    Esta função deve ser chamada por um cron job ou task scheduler
    """
    hoje = timezone.now().date()
    
    # Contas vencidas hoje
    contas_vencidas = MovimentacaoFinanceira.objects.filter(
        status='pendente',
        data_vencimento=hoje
    )
    
    for conta in contas_vencidas:
        Notification.notify_conta_vencida(conta)


# Função para limpar notificações antigas
def cleanup_old_notifications(days=30):
    """
    Remove notificações lidas mais antigas que X dias
    """
    cutoff_date = timezone.now() - timedelta(days=days)
    
    old_notifications = Notification.objects.filter(
        unread=False,
        timestamp__lt=cutoff_date
    )
    
    count = old_notifications.count()
    old_notifications.delete()
    
    return count
