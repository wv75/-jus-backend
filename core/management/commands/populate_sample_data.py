from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from clientes.models import Cliente
from processos.models import Processo
from andamentos.models import AndamentoProcessual
from templatesmsg.models import TemplateMensagem


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de exemplo...')

        # Criar usuário advogado se não existir
        advogado, created = User.objects.get_or_create(
            username='advogado1',
            defaults={
                'first_name': 'João',
                'last_name': 'Silva',
                'email': 'joao.silva@escritorio.com'
            }
        )
        if created:
            advogado.set_password('senha123')
            advogado.save()

        # Criar clientes
        clientes_data = [
            {
                'nome': 'Maria Santos Silva',
                'documento': '12345678901',
                'email': 'maria.santos@email.com',
                'telefone_whatsapp': '(11) 99999-1111',
                'consentimento_lgpd': True,
                'canal_preferido': 'whatsapp'
            },
            {
                'nome': 'José Oliveira Lima',
                'documento': '98765432100',
                'email': 'jose.oliveira@email.com',
                'telefone_whatsapp': '(11) 99999-2222',
                'consentimento_lgpd': True,
                'canal_preferido': 'email'
            }
        ]

        clientes = []
        for cliente_data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                documento=cliente_data['documento'],
                defaults=cliente_data
            )
            clientes.append(cliente)
            if created:
                self.stdout.write(f'Cliente criado: {cliente.nome}')

        # Criar processos
        processos_data = [
            {
                'numero_processo': '1234567-89.2024.8.26.0001',
                'cliente': clientes[0],
                'foro': 'Foro Central',
                'vara': '1ª Vara Cível',
                'classe': 'Ação de Cobrança',
                'assunto': 'Cobrança de valores em atraso',
                'parte_contraria': 'Empresa XYZ Ltda',
                'advogado_responsavel': advogado,
                'situacao_atual': 'Aguardando citação',
                'risco': 'medio',
                'prioridade': 'media'
            },
            {
                'numero_processo': '9876543-21.2024.8.26.0002',
                'cliente': clientes[0],
                'foro': 'Foro Regional',
                'vara': '2ª Vara Cível',
                'classe': 'Ação Trabalhista',
                'assunto': 'Rescisão indireta de contrato',
                'parte_contraria': 'Empresa ABC S.A.',
                'advogado_responsavel': advogado,
                'situacao_atual': 'Em fase de instrução',
                'risco': 'alto',
                'prioridade': 'alta'
            },
            {
                'numero_processo': '5555555-55.2024.8.26.0003',
                'cliente': clientes[1],
                'foro': 'Foro Central',
                'vara': '3ª Vara Cível',
                'classe': 'Ação de Indenização',
                'assunto': 'Danos morais e materiais',
                'parte_contraria': 'Seguradora DEF',
                'advogado_responsavel': advogado,
                'situacao_atual': 'Aguardando perícia',
                'risco': 'baixo',
                'prioridade': 'baixa'
            },
            {
                'numero_processo': '7777777-77.2024.8.26.0004',
                'cliente': clientes[1],
                'foro': 'Foro Regional',
                'vara': '1ª Vara Família',
                'classe': 'Divórcio Consensual',
                'assunto': 'Dissolução de união estável',
                'parte_contraria': '',
                'advogado_responsavel': advogado,
                'situacao_atual': 'Aguardando homologação',
                'risco': 'baixo',
                'prioridade': 'media'
            }
        ]

        processos = []
        for processo_data in processos_data:
            processo, created = Processo.objects.get_or_create(
                numero_processo=processo_data['numero_processo'],
                defaults=processo_data
            )
            processos.append(processo)
            if created:
                self.stdout.write(f'Processo criado: {processo.numero_processo}')

        # Criar andamentos
        base_date = timezone.now() - timedelta(days=30)
        andamentos_data = []
        
        for i, processo in enumerate(processos):
            for j in range(3):  # 3 andamentos por processo
                data_evento = base_date + timedelta(days=i*7 + j*2)
                andamentos_data.append({
                    'processo': processo,
                    'tipo_evento': ['peticao', 'audiencia_marcada', 'andamento_geral'][j],
                    'titulo': f'Andamento {j+1} - {processo.numero_processo}',
                    'descricao': f'Descrição detalhada do andamento {j+1} do processo {processo.numero_processo}',
                    'data_evento': data_evento,
                    'publicado_para_cliente': j % 2 == 0  # Alterna entre publicado e não publicado
                })

        for andamento_data in andamentos_data:
            andamento, created = AndamentoProcessual.objects.get_or_create(
                processo=andamento_data['processo'],
                titulo=andamento_data['titulo'],
                defaults=andamento_data
            )
            if created:
                self.stdout.write(f'Andamento criado: {andamento.titulo}')

        # Criar templates de mensagem
        templates_data = [
            {
                'canal': 'whatsapp',
                'evento': 'audiencia_marcada',
                'linguagem': 'pt-BR',
                'conteudo': 'Olá, {{primeiro_nome}}! Sua audiência do processo {{numero_processo}} foi marcada para {{data_evento_fmt}}. Compareça no horário agendado.'
            },
            {
                'canal': 'email',
                'evento': 'audiencia_marcada',
                'linguagem': 'pt-BR',
                'conteudo': 'Prezado(a) {{primeiro_nome}},\n\nInformamos que foi marcada audiência para o processo {{numero_processo}} na data {{data_evento_fmt}}.\n\nAtenciosamente,\nEscritório Jurídico'
            },
            {
                'canal': 'whatsapp',
                'evento': 'documento_solicitado',
                'linguagem': 'pt-BR',
                'conteudo': 'Olá, {{primeiro_nome}}! Precisamos de documentos para o processo {{numero_processo}}. Entre em contato conosco.'
            },
            {
                'canal': 'email',
                'evento': 'resumo_semanal',
                'linguagem': 'pt-BR',
                'conteudo': 'Prezado(a) {{primeiro_nome}},\n\nSegue resumo semanal dos seus processos:\n\nProcesso: {{numero_processo}}\nÚltimo andamento: {{data_evento_fmt}}\n\nAtenciosamente,\nEscritório Jurídico'
            }
        ]

        for template_data in templates_data:
            template, created = TemplateMensagem.objects.get_or_create(
                canal=template_data['canal'],
                evento=template_data['evento'],
                linguagem=template_data['linguagem'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'Template criado: {template.canal} - {template.evento}')

        self.stdout.write(
            self.style.SUCCESS('Dados de exemplo criados com sucesso!')
        )
