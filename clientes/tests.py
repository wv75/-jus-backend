from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cliente


class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome='João Silva',
            documento='12345678901',
            email='joao@email.com',
            telefone_whatsapp='11999999999',
            consentimento_lgpd=True
        )

    def test_cliente_creation(self):
        """Teste de criação de cliente"""
        self.assertEqual(self.cliente.nome, 'João Silva')
        self.assertEqual(self.cliente.documento, '12345678901')
        self.assertTrue(self.cliente.ativo)
        self.assertEqual(self.cliente.canal_preferido, 'whatsapp')

    def test_primeiro_nome_property(self):
        """Teste da propriedade primeiro_nome"""
        self.assertEqual(self.cliente.primeiro_nome, 'João')

    def test_str_method(self):
        """Teste do método __str__"""
        self.assertEqual(str(self.cliente), 'João Silva')


class ClienteAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.cliente = Cliente.objects.create(
            nome='Maria Silva',
            documento='98765432100',
            email='maria@email.com',
            telefone_whatsapp='11888888888'
        )

    def test_api_requires_authentication(self):
        """Teste que API requer autenticação"""
        response = self.client.get('/api/clientes/')
        self.assertEqual(response.status_code, 403)

    def test_api_with_authentication(self):
        """Teste de acesso à API com autenticação"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/clientes/')
        self.assertEqual(response.status_code, 200)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_landing_page(self):
        """Teste da landing page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """Teste da página de login"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        """Teste que dashboard requer login"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_with_login(self):
        """Teste do dashboard com usuário logado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
