'''
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from clientes.models import Cliente
from processos.models import Processo
from agenda.models import Compromisso
from financeiro.models import MovimentacaoFinanceira, Honorario
from notifications.models import Notification
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
class TestIntegracaoCompleta(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_vinculo_multiplo_usuarios_cliente(self):
        user2 = User.objects.create_user(username='testuser2', password='testpassword')
        cliente = Cliente.objects.create(nome='Cliente Teste', documento='12345678901', email='teste@teste.com', telefone_whatsapp='11999999999')
        cliente.usuarios.add(self.user, user2)
        self.assertEqual(cliente.usuarios.count(), 2)

    def test_integracao_processo_agenda(self):
        cliente = Cliente.objects.create(nome='Cliente Processo', documento='12345678902', email='processo@teste.com', telefone_whatsapp='11999999998')
        prazo = timezone.now() + timedelta(days=10)
        processo = Processo.objects.create(
            cliente=cliente,
            numero_processo='1234567-89.2023.1.01.0001',
            status='novo',
            prazo_final=prazo.date()
        )
        compromisso = Compromisso.objects.get(processo_relacionado=processo)
        self.assertEqual(compromisso.titulo, f"Prazo do processo {processo.numero_processo}")
        self.assertEqual(compromisso.data_inicio.date(), prazo.date())

    def test_crud_financeiro(self):
        response = self.client.get(reverse('financeiro:movimentacao_list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('financeiro:honorario_list'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_com_dados_reais(self):
        response = self.client.get(reverse('dashboard:executivo'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard Executivo")
        response = self.client.get(reverse('dashboard:operacional'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard Operacional")

    def test_protecao_de_rotas(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard:executivo'), follow=True)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard:executivo')}")

    def test_notificacao_novo_processo(self):
        cliente = Cliente.objects.create(nome='Cliente Notificacao', documento='12345678903', email='notificacao@teste.com', telefone_whatsapp='11999999997')
        Processo.objects.create(
            cliente=cliente,
            numero_processo='9876543-21.2023.1.01.0001',
            status='novo'
        )
        notification = Notification.objects.get(processo__numero_processo='9876543-21.2023.1.01.0001')
        self.assertEqual(notification.verb, "Novo processo criado")
'''
