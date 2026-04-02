import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from processos.models import Processo
from documentos.models import Documento, CategoriaDocumento
from agenda.models import Compromisso
from financeiro.models import MovimentacaoFinanceira, Honorario, PlanoContas, ContaBancaria
from notifications.models import Notification
from clientes.models import Cliente

@pytest.mark.django_db
class TestIntegracaoV2(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password', is_staff=True)
        self.client.login(username='testuser', password='password')
        self.cliente = Cliente.objects.create(nome='Cliente Teste', documento='12345678901')
        self.categoria = CategoriaDocumento.objects.create(nome='Categoria Teste')
        self.plano_conta_receita = PlanoContas.objects.create(codigo='1.01', nome='Receitas', tipo='receita')
        self.plano_conta_despesa = PlanoContas.objects.create(codigo='2.01', nome='Despesas', tipo='despesa')
        self.conta_bancaria = ContaBancaria.objects.create(nome='Conta Principal', banco='Banco Teste', agencia='0001', conta='12345-6')

    def test_criacao_compromisso_automatico_processo(self):
        processo = Processo.objects.create(
            cliente=self.cliente,
            numero_processo='123456',
            status='novo',
            prioridade='alta',
            advogado_responsavel=self.user
        )
        compromisso_exists = Compromisso.objects.filter(processo_relacionado=processo).exists()
        self.assertTrue(compromisso_exists)

    def test_criacao_compromisso_automatico_documento(self):
        documento = Documento.objects.create(
            cliente=self.cliente,
            titulo='Documento Teste',
            tipo='contrato',
            categoria=self.categoria,
            autor=self.user
        )
        compromisso_exists = Compromisso.objects.filter(titulo__contains='Revisar documento').exists()
        self.assertTrue(compromisso_exists)

    def test_crud_financeiro(self):
        # Testar criação de receita
        response = self.client.post(reverse('financeiro:nova_receita'), {
            'descricao': 'Receita Teste',
            'valor': 100.00,
            'data_vencimento': '2025-12-31',
            'cliente': self.cliente.id,
            'plano_conta': self.plano_conta_receita.id,
            'conta_bancaria': self.conta_bancaria.id,
            'tipo': 'receita',
            'status': 'pendente'
        })
        self.assertEqual(response.status_code, 302, "A criação de receita falhou na validação do formulário.")
        self.assertTrue(MovimentacaoFinanceira.objects.filter(descricao='Receita Teste').exists())

        # Testar criação de despesa
        response = self.client.post(reverse('financeiro:nova_despesa'), {
            'descricao': 'Despesa Teste',
            'valor': 50.00,
            'data_vencimento': '2025-12-31',
            'cliente': self.cliente.id,
            'plano_conta': self.plano_conta_despesa.id,
            'conta_bancaria': self.conta_bancaria.id,
            'tipo': 'despesa',
            'status': 'pendente'
        })
        self.assertEqual(response.status_code, 302, "A criação de despesa falhou na validação do formulário.")
        self.assertTrue(MovimentacaoFinanceira.objects.filter(descricao='Despesa Teste').exists())

        # Testar criação de honorário
        processo = Processo.objects.create(cliente=self.cliente, numero_processo='654321', advogado_responsavel=self.user)
        response = self.client.post(reverse('financeiro:novo_honorario'), {
            'descricao': 'Honorário Teste',
            'valor': 200.00,
            'cliente': self.cliente.id,
            'processo': processo.id,
            'advogado': self.user.id,
            'tipo': 'fixo',
            'status': 'orcamento',
            'data_vencimento': '2025-12-31'
        })
        self.assertEqual(response.status_code, 302, "A criação de honorário falhou na validação do formulário.")
        self.assertTrue(Honorario.objects.filter(descricao='Honorário Teste').exists())

    def test_dashboard_executivo(self):
        response = self.client.get(reverse('dashboard:executivo'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard Executivo')

    def test_dashboard_operacional(self):
        response = self.client.get(reverse('dashboard:operacional'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard Operacional')

    def test_notificacoes_expandidas(self):
        Notification.objects.create(
            recipient=self.user,
            verb='Teste',
            modulo='sistema',
            status='ativa'
        )
        response = self.client.get(reverse('notifications:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Teste')

